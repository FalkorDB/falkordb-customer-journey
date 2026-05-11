"""Generate a DB deletion follow-up email with Grafana data + screenshot.

Run `python generate_message.py --help` for options. See README.md in this
directory for the full overview.
"""
from __future__ import annotations

import argparse
import logging
import mimetypes
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
class GrafanaMetrics:
    total_queries: Optional[int] = None
    peak_qps: Optional[float] = None
    node_count_last: Optional[int] = None
    edge_count_last: Optional[int] = None
    screenshot_path: Optional[Path] = None

    @property
    def has_screenshot(self) -> bool:
        return self.screenshot_path is not None and self.screenshot_path.exists()


def parse_iso(ts: str) -> datetime:
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
) -> GrafanaMetrics:
    if dry_run:
        logger.info("Dry-run: using sample metrics, skipping Grafana calls.")
        sample_png = out_dir / f"{out_stem}.png"
        # Write a 1x1 transparent PNG so the .eml has a valid attachment to inline.
        sample_png.write_bytes(
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
            b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\xcf"
            b"\xc0\xf0\x1f\x00\x05\x00\x01\xff\xa7\xf5j\xb1\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        return GrafanaMetrics(
            total_queries=184_302,
            peak_qps=47.0,
            node_count_last=1_200_000,
            edge_count_last=4_800_000,
            screenshot_path=sample_png,
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
        screenshot_path=screenshot_path,
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
    screenshot_path: Optional[Path],
) -> bytes:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{config['email']['from_name']} <{config['email']['from_address']}>"
    msg["To"] = recipient or "REPLACE_WITH_RECIPIENT@example.com"
    msg["Reply-To"] = config["email"]["reply_to"]

    msg.set_content(body_markdown)

    if screenshot_path and screenshot_path.exists():
        mime_type, _ = mimetypes.guess_type(str(screenshot_path))
        maintype, subtype = (mime_type or "image/png").split("/", 1)
        cid = make_msgid(domain="falkordb.local")
        cid_value = cid.strip("<>")
        html_body = (
            "<html><body><pre style='font-family:inherit;white-space:pre-wrap'>"
            + body_markdown.replace("cid:grafana-screenshot", f"cid:{cid_value}")
            + "</pre></body></html>"
        )
        msg.add_alternative(html_body, subtype="html")
        with screenshot_path.open("rb") as fh:
            msg.get_payload()[1].add_related(
                fh.read(),
                maintype=maintype,
                subtype=subtype,
                cid=cid,
                filename=screenshot_path.name,
            )

    return bytes(msg)


def load_config(path: Path) -> dict[str, Any]:
    with path.open() as fh:
        return yaml.safe_load(fh)


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--db-name", required=True)
    parser.add_argument("--first-name", required=True)
    parser.add_argument("--created-at", required=True, help="ISO 8601, e.g. 2026-03-15T09:00:00Z")
    parser.add_argument("--deleted-at", required=True, help="ISO 8601")
    parser.add_argument("--recipient", default=None, help="Recipient email for the .eml")
    parser.add_argument("--out-dir", type=Path, default=Path("./out"))
    parser.add_argument("--variant", choices=["a", "b"], default=None, help="Force variant for testing")
    parser.add_argument(
        "--screenshot",
        type=Path,
        default=None,
        help="Path to a local PNG to inline as the Grafana screenshot. "
             "Overrides the Grafana /render fetch. Useful when you've exported "
             "the panel manually.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Skip Grafana, use sample data")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    config = load_config(args.config)
    created_at = parse_iso(args.created_at)
    deleted_at = parse_iso(args.deleted_at)
    if deleted_at < created_at:
        logger.error("deleted_at is before created_at")
        return 2

    args.out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_stem = f"{args.db_name}_{timestamp}"

    metrics = collect_metrics(
        config=config,
        db_name=args.db_name,
        created_at=created_at,
        deleted_at=deleted_at,
        out_dir=args.out_dir,
        out_stem=out_stem,
        dry_run=args.dry_run,
    )

    if args.screenshot:
        if not args.screenshot.exists():
            logger.error("--screenshot path does not exist: %s", args.screenshot)
            return 2
        target = args.out_dir / f"{out_stem}{args.screenshot.suffix}"
        target.write_bytes(args.screenshot.read_bytes())
        metrics.screenshot_path = target
        logger.info("Using local screenshot: %s", args.screenshot)

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
        screenshot_path=metrics.screenshot_path if variant == "a" else None,
    )
    eml_path.write_bytes(eml_bytes)

    print(f"Wrote: {md_path}")
    print(f"Wrote: {eml_path}")
    if metrics.screenshot_path:
        print(f"Wrote: {metrics.screenshot_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
