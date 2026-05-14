# DB Deletion Follow-Up — With Usage
**Trigger:** User deletes a FalkorDB Cloud database that had meaningful activity
**Send timing:** Within 24 hours of deletion
**Tone:** Warm, low-pressure, genuinely curious — not a save-the-sale email
**Routing rule:** Deleted DB had **≥ 1,000 queries lifetime** OR **≥ 7 days of activity**

---

## Purpose

When a user deletes a Cloud database that they actually used, we want to learn
*why* and give them a low-friction way to tell us. The message acknowledges the
real work the DB did (lifetime, query volume, graph size) and asks one short
question. No save-the-sale energy.

**Suppression:**
- Do **not** send if the user still has another active DB on the account (use a "downsize" message instead).
- Do **not** send if the account itself was closed (deletion was incidental).
- Do **not** send if a deletion follow-up was already sent in the last 30 days.

---

## Tokens / data fields

Pulled from the Cloud control plane and Grafana before send. Leave blank /
omit the line if data is unavailable.

| Token | Source | Example |
|---|---|---|
| `{db_name}` | Cloud control plane | `prod-graph-01` |
| `{db_lifetime_days}` | Cloud control plane | `42` |
| `{total_queries}` | Grafana — queries panel | `184,302` |
| `{peak_qps}` | Grafana — QPS panel | `47` |
| `{node_count_last}` | Grafana — graph size panel | `1.2M` |
| `{edge_count_last}` | Grafana — graph size panel | `4.8M` |
| `{grafana_screenshot_url}` | Rendered PNG from Grafana share link | https://… |

**Embedding the screenshot:** attach the PNG inline (CID) with descriptive
`alt` text, e.g. *"Daily query volume for prod-graph-01 over its lifetime."*
Always include the numeric fallback line below the image for clients that
block images. If the screenshot URL is null at send time, drop the image
block entirely — don't ship a broken image icon.

---

## Subject

You deleted {db_name} — mind sharing what happened?

---

## Body

Hi {First Name},

We noticed you deleted **{db_name}** on FalkorDB Cloud yesterday. No worries at all — we just wanted to check in.

Over its {db_lifetime_days} days running, that database handled **{total_queries} queries** (peaking at {peak_qps} QPS) and grew to **{node_count_last} nodes / {edge_count_last} edges**. That's real work — so before you go, we'd genuinely love to know what happened.

> **[Inline Grafana screenshot: lifetime query volume for {db_name}]**
> *Daily queries over the lifetime of {db_name}. (If you don't see the image, here's the summary: {total_queries} queries across {db_lifetime_days} days, peak {peak_qps} QPS.)*

A one-line reply to any of these helps us a lot:

- **Project ended** — totally fine, thanks for using us.
- **Migrated to another DB** — which one, and what tipped the scales?
- **Hit a limitation** — performance, a missing feature, pricing, ops?
- **Just testing** — what would have made you keep going?

No follow-up sequence, no sales call — just one human reading the reply.

If you want to spin something new up later, your account is still active and **[the Cloud Console](https://app.falkordb.cloud)** is one click away. And if you'd like to chat with an engineer (not a CSM) about a specific issue, reply with "engineer" and we'll set it up.

Thanks for giving FalkorDB a shot.

— The FalkorDB Team

---

*You're receiving this because you recently deleted a database on FalkorDB Cloud. You can reply to opt out of future check-ins.*

---

## Implementation notes

- **Send from a real person's address** (e.g., founder or DevRel), not `noreply@`. Reply rate roughly doubles on this kind of message when it looks personal.
- **Plain-text alternative required** alongside the HTML/Grafana-image version, listing the same numbers.
- **Tracking:** tag replies with `deletion-followup-with-usage-v1` and bucket by reason category so we can report monthly on top deletion drivers.
