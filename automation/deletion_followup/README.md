# Deletion Follow-Up Message Generator

Generates the "DB Deletion Follow-Up" lifecycle message
(`messages/db_deletion_followup_v1.md`) with real data: pulls metrics from
Grafana's Prometheus datasource proxy, renders a Grafana panel as a PNG, and
produces both a Markdown preview and an `.eml` file with the screenshot inlined
as a CID attachment.

The output is intended for **manual review and send** — no SMTP, no HubSpot API
calls. Generate, eyeball, then forward via your normal mail client.

## Layout

```
automation/deletion_followup/
├── generate_message.py        # Entry point
├── config.example.yaml        # Copy to config.yaml and fill in
├── requirements.txt
├── templates/
│   ├── with_usage.md.j2       # Variant A
│   └── without_usage.md.j2    # Variant B
└── tests/
    └── test_generate_message.py
```

## Install

```bash
cd automation/deletion_followup
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp config.example.yaml config.yaml   # then edit
```

`config.yaml` is gitignored — it holds your Grafana token. Never commit it.

## Run

```bash
python generate_message.py \
  --config config.yaml \
  --db-name prod-graph-01 \
  --first-name Alex \
  --created-at 2026-03-15T09:00:00Z \
  --deleted-at 2026-05-10T17:42:00Z \
  --out-dir ./out
```

## Where to put the Grafana screenshot

**Keep the screenshot outside this repo.** Production dashboard images can
leak instance names, customer identifiers, and traffic patterns — they should
never be at risk of being committed.

Recommended location: a folder in your home directory, e.g.

```bash
mkdir -p ~/falkordb-screenshots
```

You have three options for the image, in order of recommended workflow:

1. **Export the PNG manually and pass `--screenshot`** *(recommended for the first runs)*
   ```bash
   # 1. In Grafana, open the panel → Share → Direct link rendered image,
   #    OR Panel menu → Inspect → Panel JSON → screenshot.
   # 2. Save the PNG anywhere outside this repo, e.g.:
   #      ~/falkordb-screenshots/prod-graph-01.png
   # 3. Run with --screenshot pointing at the absolute path:
   python generate_message.py --config config.yaml \
     --db-name prod-graph-01 --first-name Alex \
     --created-at 2026-03-15T09:00:00Z --deleted-at 2026-05-10T17:42:00Z \
     --screenshot ~/falkordb-screenshots/prod-graph-01.png \
     --out-dir ./out
   ```
   The file is copied into `out/<db_name>_<timestamp>.png` (which is gitignored)
   and CID-inlined in the `.eml`. The original stays where you put it.

2. **Let the script fetch it from Grafana's `/render` API** — requires the
   [Grafana Image Renderer plugin](https://grafana.com/grafana/plugins/grafana-image-renderer/)
   installed on your Grafana server. No CLI flag needed; it happens automatically
   if `--screenshot` is omitted and `--dry-run` is not set.

3. **Skip the image entirely** — pass neither `--screenshot` nor real Grafana
   credentials. The template falls back to the numeric summary line only
   (no broken image icon).

Outputs:

- `out/<db_name>_<timestamp>.md` — rendered Markdown for review.
- `out/<db_name>_<timestamp>.eml` — RFC 822 message with the Grafana PNG
  inlined (Content-ID: `grafana-screenshot`) plus a plain-text alternative.
- `out/<db_name>_<timestamp>.png` — the raw panel render, kept for the record.

Variant selection is automatic based on the thresholds in `config.yaml`
(default: ≥ 1,000 queries lifetime OR ≥ 7 days active → Variant A, else B).
Force a variant with `--variant a|b` for testing.

## How the data is gathered

| Field | Source |
|---|---|
| `total_queries` | PromQL `sum(increase(<queries_metric>{db="<name>"}[<lifetime>]))` |
| `peak_qps` | PromQL `max_over_time(rate(<queries_metric>{db="<name>"}[1m])[<lifetime>:])` |
| `node_count_last` | PromQL `<nodes_metric>{db="<name>"}` (last value) |
| `edge_count_last` | PromQL `<edges_metric>{db="<name>"}` (last value) |
| `db_lifetime_days` | Derived from `--created-at` and `--deleted-at` |
| Grafana screenshot | `GET /render/d-solo/<dashboard_uid>?panelId=<id>&from=<created>&to=<deleted>&width=1000&height=400` |

Metric names and the dashboard/panel IDs are configured in `config.yaml` so
this works with whatever Prometheus schema your Cloud control plane exposes.

## Failure modes (handled, not fatal)

- **Prometheus query returns empty / errors** → that metric is set to `None`
  and its line is omitted from the rendered message.
- **Grafana render endpoint unavailable** (no image renderer installed) →
  PNG is skipped; the inline image block is replaced with the numeric summary
  fallback already specified in the template.
- **Both metrics and image unavailable** → falls through to Variant B.

## Testing

```bash
pytest tests/
```
