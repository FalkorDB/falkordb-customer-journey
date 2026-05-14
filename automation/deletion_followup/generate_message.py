"""Generate a DB deletion follow-up email with Grafana data + screenshot.

Run `python generate_message.py --help` for options. See README.md in this
directory for the full overview.
"""
from __future__ import annotations

import argparse
import json
import logging
import mimetypes
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path
from typing import Any, Optional

import requests
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

logger = logging.getLogger("deletion_followup")

TEMPLATES_DIR = Path(__file__).parent / "templates"


@dataclass
class InstanceOwner:
    instance_id: str
    db_name: Optional[str]
    owner_email: Optional[str]
    owner_name: Optional[str]
    instance_start_date: Optional[str]
    instance_status: Optional[str]


def resolve_instance_owner(snapshot_path: Path, instance_id: str) -> InstanceOwner:
    """Look up an instance in the local Omnistrate snapshot.

    Snapshot is produced by ~/Documents/work/hubspot-utils/export_omnistrate_instances.py.
    Raises FileNotFoundError if the snapshot is missing, KeyError if the id isn't there.
    """
    if not snapshot_path.exists():
        raise FileNotFoundError(
            f"Instance snapshot not found at {snapshot_path}. "
            "Run ~/Documents/work/hubspot-utils/export_omnistrate_instances.py "
            "to generate it, or set instance_snapshot_path in config.yaml."
        )
    data = json.loads(snapshot_path.read_text())
    instances = data.get("instances") if isinstance(data, dict) else data
    if not isinstance(instances, list):
        raise ValueError(f"Unexpected snapshot shape in {snapshot_path}")
    for inst in instances:
        if inst.get("instance_name") == instance_id or inst.get("subscription_id") == instance_id:
            return InstanceOwner(
                instance_id=instance_id,
                db_name=inst.get("db_name"),
                owner_email=inst.get("owner_email"),
                owner_name=inst.get("owner_name"),
                instance_start_date=inst.get("instance_start_date"),
                instance_status=inst.get("instance_status"),
            )
    raise KeyError(
        f"instance_id={instance_id!r} not found in snapshot {snapshot_path}. "
        "If the instance was created recently, refresh the snapshot."
    )


def first_name_from_owner_name(owner_name: Optional[str]) -> str:
    """Extract the first token from a free-form owner name. Falls back to 'there'."""
    if not owner_name:
        return "there"
    parts = owner_name.strip().split()
    return parts[0] if parts else "there"


@dataclass
class GrafanaMetrics:
    total_queries: Optional[int] = None
    peak_qps: Optional[float] = None
    node_count_last: Optional[int] = None
    edge_count_last: Optional[int] = None
    screenshot_paths: list[Path] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.screenshot_paths is None:
            self.screenshot_paths = []

    @property
    def has_screenshot(self) -> bool:
        return any(p.exists() for p in self.screenshot_paths)


def slugify(value: str) -> str:
    """Conservative slug for filenames: lowercase, alnum and dashes only."""
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return cleaned or "unknown"


def parse_iso(ts: str) -> datetime:
    # Accept epoch milliseconds (Omnistrate snapshot format).
    if isinstance(ts, str) and ts.isdigit():
        return datetime.fromtimestamp(int(ts) / 1000.0, tz=timezone.utc)
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(float(ts) / 1000.0, tz=timezone.utc)
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts).astimezone(timezone.utc)


def format_number(value: Optional[float]) -> Optional[str]:
    if value is None:
        return None
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value:,.0f}"
    return f"{value:.0f}" if value == int(value) else f"{value:.1f}"


def humanize_when(deleted_at: datetime, now: Optional[datetime] = None) -> str:
    now = now or datetime.now(timezone.utc)
    delta_hours = (now - deleted_at).total_seconds() / 3600
    if delta_hours < 1:
        return "earlier today"
    if delta_hours < 24:
        return "earlier today"
    if delta_hours < 48:
        return "yesterday"
    return f"{int(delta_hours / 24)} days ago"


def query_prometheus_instant(
    base_url: str,
    api_token: str,
    datasource_uid: str,
    promql: str,
    timeout: int,
) -> Optional[float]:
    url = (
        f"{base_url.rstrip('/')}/api/datasources/proxy/uid/"
        f"{datasource_uid}/api/v1/query"
    )
    try:
        response = requests.get(
            url,
            params={"query": promql},
            headers={"Authorization": f"Bearer {api_token}"},
            timeout=timeout,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.warning("Prometheus query failed (%s): %s", promql, exc)
        return None

    payload = response.json()
    if payload.get("status") != "success":
        logger.warning("Prometheus returned non-success for %s: %s", promql, payload)
        return None

    result = payload.get("data", {}).get("result", [])
    if not result:
        return None
    try:
        return float(result[0]["value"][1])
    except (KeyError, IndexError, ValueError):
        return None


def fetch_grafana_panel_png(
    base_url: str,
    api_token: str,
    dashboard_uid: str,
    panel_id: int,
    from_dt: datetime,
    to_dt: datetime,
    width: int,
    height: int,
    timeout: int,
    output_path: Path,
) -> Optional[Path]:
    url = f"{base_url.rstrip('/')}/render/d-solo/{dashboard_uid}"
    params = {
        "panelId": panel_id,
        "from": int(from_dt.timestamp() * 1000),
        "to": int(to_dt.timestamp() * 1000),
        "width": width,
        "height": height,
        "tz": "UTC",
    }
    try:
        response = requests.get(
            url,
            params=params,
            headers={"Authorization": f"Bearer {api_token}"},
            timeout=timeout,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.warning("Grafana render failed: %s", exc)
        return None

    content_type = response.headers.get("Content-Type", "")
    if "image" not in content_type:
        logger.warning("Grafana render returned non-image content-type: %s", content_type)
        return None

    output_path.write_bytes(response.content)
    return output_path


def collect_metrics(
    config: dict[str, Any],
    db_name: str,
    created_at: datetime,
    deleted_at: datetime,
    out_dir: Path,
    out_stem: str,
    dry_run: bool,
    write_placeholder_image: bool = True,
) -> GrafanaMetrics:
    if dry_run:
        logger.info("Dry-run: using sample metrics, skipping Grafana calls.")
        screenshot_paths: list[Path] = []
        if write_placeholder_image:
            sample_png = out_dir / f"{out_stem}.png"
            sample_png.write_bytes(
                b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
                b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\xcf"
                b"\xc0\xf0\x1f\x00\x05\x00\x01\xff\xa7\xf5j\xb1\x00\x00\x00\x00IEND\xaeB`\x82"
            )
            screenshot_paths = [sample_png]
        return GrafanaMetrics(
            total_queries=184_302,
            peak_qps=47.0,
            node_count_last=1_200_000,
            edge_count_last=4_800_000,
            screenshot_paths=screenshot_paths,
        )

    gconf = config["grafana"]
    metric_names = config["prometheus_metrics"]
    db_label = metric_names["db_label"]
    lifetime_seconds = max(int((deleted_at - created_at).total_seconds()), 60)

    selector = f'{{{db_label}="{db_name}"}}'
    queries = {
        "total_queries": (
            f"sum(increase({metric_names['queries_total']}{selector}"
            f"[{lifetime_seconds}s]))"
        ),
        "peak_qps": (
            f"max_over_time(rate({metric_names['queries_total']}{selector}"
            f"[1m])[{lifetime_seconds}s:])"
        ),
        "node_count_last": f"{metric_names['nodes']}{selector}",
        "edge_count_last": f"{metric_names['edges']}{selector}",
    }

    results: dict[str, Optional[float]] = {}
    for field, promql in queries.items():
        results[field] = query_prometheus_instant(
            base_url=gconf["base_url"],
            api_token=gconf["api_token"],
            datasource_uid=gconf["datasource_uid"],
            promql=promql,
            timeout=gconf["request_timeout_seconds"],
        )

    screenshot_path = fetch_grafana_panel_png(
        base_url=gconf["base_url"],
        api_token=gconf["api_token"],
        dashboard_uid=gconf["dashboard_uid"],
        panel_id=gconf["panel_id"],
        from_dt=created_at,
        to_dt=deleted_at,
        width=gconf["render_width"],
        height=gconf["render_height"],
        timeout=gconf["request_timeout_seconds"],
        output_path=out_dir / f"{out_stem}.png",
    )

    return GrafanaMetrics(
        total_queries=int(results["total_queries"]) if results["total_queries"] else None,
        peak_qps=round(results["peak_qps"], 1) if results["peak_qps"] else None,
        node_count_last=int(results["node_count_last"]) if results["node_count_last"] else None,
        edge_count_last=int(results["edge_count_last"]) if results["edge_count_last"] else None,
        screenshot_paths=[screenshot_path] if screenshot_path else [],
    )


def choose_variant(
    metrics: GrafanaMetrics,
    db_lifetime_days: int,
    thresholds: dict[str, int],
    forced: Optional[str],
) -> str:
    if forced in {"a", "b"}:
        return forced
    has_enough_queries = (metrics.total_queries or 0) >= thresholds["min_total_queries"]
    has_enough_days = db_lifetime_days >= thresholds["min_active_days"]
    return "a" if (has_enough_queries or has_enough_days) else "b"


def render_message(
    variant: str,
    context: dict[str, Any],
) -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        undefined=StrictUndefined,
        trim_blocks=False,
        lstrip_blocks=False,
    )
    template_name = "with_usage.md.j2" if variant == "a" else "without_usage.md.j2"
    template = env.get_template(template_name)
    return template.render(**context)


def build_eml(
    subject: str,
    body_markdown: str,
    config: dict[str, Any],
    recipient: Optional[str],
    screenshot_paths: list[Path],
) -> bytes:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{config['email']['from_name']} <{config['email']['from_address']}>"
    msg["To"] = recipient or "REPLACE_WITH_RECIPIENT@example.com"
    msg["Reply-To"] = config["email"]["reply_to"]

    msg.set_content(body_markdown)

    valid_paths = [p for p in screenshot_paths if p.exists()]
    if valid_paths:
        html_body = body_markdown
        cids: list[tuple[str, Path, str]] = []
        for idx, path in enumerate(valid_paths, start=1):
            mime_type, _ = mimetypes.guess_type(str(path))
            maintype, subtype = (mime_type or "image/png").split("/", 1)
            cid = make_msgid(domain="falkordb.local")
            cid_value = cid.strip("<>")
            placeholder = f"cid:grafana-screenshot-{idx}"
            html_body = html_body.replace(placeholder, f"cid:{cid_value}")
            cids.append((cid, path, f"{maintype}/{subtype}"))

        html_wrapped = (
            "<html><body><pre style='font-family:inherit;white-space:pre-wrap'>"
            + html_body
            + "</pre></body></html>"
        )
        msg.add_alternative(html_wrapped, subtype="html")
        html_part = msg.get_payload()[1]
        for cid, path, mime in cids:
            maintype, subtype = mime.split("/", 1)
            with path.open("rb") as fh:
                html_part.add_related(
                    fh.read(),
                    maintype=maintype,
                    subtype=subtype,
                    cid=cid,
                    filename=path.name,
                )

    return bytes(msg)


def load_config(path: Path) -> dict[str, Any]:
    with path.open() as fh:
        return yaml.safe_load(fh)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument(
        "--instance-id",
        default=None,
        help="Omnistrate instance id (e.g. instance-r2hgbez8z). "
             "Auto-fills --first-name, --recipient, --db-name from the snapshot.",
    )
    parser.add_argument("--db-name", default=None)
    parser.add_argument("--first-name", default=None)
    parser.add_argument("--created-at", default=None, help="ISO 8601; defaults to instance_start_date")
    parser.add_argument("--deleted-at", default=None, help="ISO 8601; defaults to now")
    parser.add_argument("--recipient", default=None, help="Recipient email for the .eml")
    parser.add_argument("--out-dir", type=Path, default=Path("./out"))
    parser.add_argument("--variant", choices=["a", "b"], default=None, help="Force variant for testing")
    parser.add_argument(
        "--screenshot",
        type=Path,
        action="append",
        default=None,
        help="Path to a local PNG to inline as a Grafana screenshot. "
             "Pass multiple times for multiple images (they will be inlined in order). "
             "Overrides the Grafana /render fetch.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Skip Grafana, use sample data")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    config = load_config(args.config)

    if args.instance_id:
        snapshot_path = Path(config.get("instance_snapshot_path", "")).expanduser()
        try:
            owner = resolve_instance_owner(snapshot_path, args.instance_id)
        except (FileNotFoundError, KeyError, ValueError) as exc:
            logger.error("Instance lookup failed: %s", exc)
            return 2
        logger.info(
            "Resolved %s -> %s <%s> (db_name=%s, status=%s)",
            args.instance_id, owner.owner_name, owner.owner_email,
            owner.db_name, owner.instance_status,
        )
        if not args.first_name:
            args.first_name = first_name_from_owner_name(owner.owner_name)
        if not args.recipient:
            args.recipient = owner.owner_email
        if not args.db_name:
            args.db_name = owner.db_name or args.instance_id
        if not args.created_at and owner.instance_start_date:
            args.created_at = owner.instance_start_date

    if not args.deleted_at:
        args.deleted_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    missing = [name for name, val in
               (("--db-name", args.db_name), ("--first-name", args.first_name),
                ("--created-at", args.created_at)) if not val]
    if missing:
        parser.error(f"missing required values: {', '.join(missing)} "
                     "(supply directly or use --instance-id)")

    created_at = parse_iso(args.created_at)
    deleted_at = parse_iso(args.deleted_at)
    if deleted_at < created_at:
        logger.error("deleted_at is before created_at")
        return 2

    args.out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_stem = f"{slugify(args.first_name)}_{slugify(args.db_name)}_{timestamp}"

    metrics = collect_metrics(
        config=config,
        db_name=args.db_name,
        created_at=created_at,
        deleted_at=deleted_at,
        out_dir=args.out_dir,
        out_stem=out_stem,
        dry_run=args.dry_run,
        write_placeholder_image=not args.screenshot,
    )

    if args.screenshot:
        copied: list[Path] = []
        for idx, src in enumerate(args.screenshot, start=1):
            if not src.exists():
                logger.error("--screenshot path does not exist: %s", src)
                return 2
            suffix = src.suffix or ".png"
            target = args.out_dir / f"{out_stem}_{idx}{suffix}"
            target.write_bytes(src.read_bytes())
            copied.append(target)
            logger.info("Using local screenshot %d: %s", idx, src)
        metrics.screenshot_paths = copied

    db_lifetime_days = max(int((deleted_at - created_at).total_seconds() / 86400), 1)
    variant = choose_variant(
        metrics=metrics,
        db_lifetime_days=db_lifetime_days,
        thresholds=config["variant_thresholds"],
        forced=args.variant,
    )
    logger.info("Selected variant: %s", variant.upper())

    context = {
        "first_name": args.first_name,
        "db_name": args.db_name,
        "db_lifetime_days": db_lifetime_days,
        "when_phrase": humanize_when(deleted_at),
        "total_queries": format_number(metrics.total_queries),
        "peak_qps": format_number(metrics.peak_qps),
        "node_count_last": format_number(metrics.node_count_last),
        "edge_count_last": format_number(metrics.edge_count_last),
        "has_screenshot": variant == "a" and metrics.has_screenshot,
        "screenshot_count": len(metrics.screenshot_paths) if variant == "a" else 0,
        "console_url": config["console_url"],
        "first_graph_guide_url": config["first_graph_guide_url"],
    }

    body = render_message(variant, context)
    subject = (
        f"You deleted {args.db_name} — mind sharing what happened?"
        if variant == "a"
        else "Anything we could have done better?"
    )

    md_path = args.out_dir / f"{out_stem}.md"
    md_path.write_text(f"# Subject: {subject}\n\n{body}", encoding="utf-8")

    eml_path = args.out_dir / f"{out_stem}.eml"
    eml_bytes = build_eml(
        subject=subject,
        body_markdown=body,
        config=config,
        recipient=args.recipient,
        screenshot_paths=metrics.screenshot_paths if variant == "a" else [],
    )
    eml_path.write_bytes(eml_bytes)

    print(f"Wrote: {md_path}")
    print(f"Wrote: {eml_path}")
    for p in metrics.screenshot_paths:
        print(f"Wrote: {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
