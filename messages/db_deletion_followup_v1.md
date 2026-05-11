# DB Deletion Follow-Up
**Trigger:** User deletes an existing FalkorDB Cloud database
**Send timing:** Within 24 hours of deletion
**Tone:** Warm, low-pressure, genuinely curious — not a save-the-sale email

---

## Purpose

When a user deletes a Cloud database, we lose visibility into *why*. This message asks — briefly — and gives us a chance to learn, recover the relationship, and improve the product. Two variants below depending on whether the deleted DB had meaningful usage.

**Routing rule (suggested):**
- If the DB had **≥ 1,000 queries lifetime** OR **≥ 7 days of activity** → send **Variant A (With Usage)**.
- Otherwise → send **Variant B (Without Usage)**.

**Suppression:**
- Do **not** send if the user still has another active DB on the account (use a different "downsize" message instead).
- Do **not** send if the account itself was closed (deletion was incidental).
- Do **not** send if a deletion follow-up was already sent in the last 30 days.

---

## Optional attachments / inline content

Both variants can be enriched with instance-specific context pulled from our Grafana dashboards before send. Keep it factual, not guilt-trippy — the goal is to show "we paid attention," not "look what you're losing."

Suggested fields to interpolate (leave blank/omit the section if data is unavailable):

| Token | Source | Example |
|---|---|---|
| `{db_name}` | Cloud control plane | `prod-graph-01` |
| `{db_lifetime_days}` | Cloud control plane | `42` |
| `{total_queries}` | Grafana — queries panel | `184,302` |
| `{peak_qps}` | Grafana — QPS panel | `47` |
| `{node_count_last}` | Grafana — graph size panel | `1.2M` |
| `{edge_count_last}` | Grafana — graph size panel | `4.8M` |
| `{grafana_screenshot_url}` | Rendered PNG from Grafana share link | https://… |

> **Embedding the screenshot:** attach the PNG inline (most email clients render it) with `alt` text describing what's shown, e.g. *"Daily query volume for prod-graph-01 over its lifetime."* Always include a text fallback line below the image for clients that block images.

---

# Variant A — With Usage

**Subject:** You deleted {db_name} — mind sharing what happened?

---

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

# Variant B — Without Usage

**Subject:** Anything we could have done better?

---

Hi {First Name},

We saw you deleted your FalkorDB Cloud database **{db_name}** before really putting it through its paces. That's completely fine — but if you have 30 seconds, we'd love to know what got in the way.

Was it:

- 🧭 **Hard to get started** — setup, connection, first query?
- 🤔 **Not what you expected** — wrong fit, different need?
- 📚 **Docs unclear** — couldn't find what you were looking for?
- ⏸️ **Just exploring** — saving it for later, no problem at all?

Even a one-word reply helps us improve onboarding for the next person.

If you'd like another go with a more guided walkthrough, our **[First Graph guide](https://docs.falkordb.com/getting-started/)** takes about 10 minutes end-to-end, and you can spin up a fresh free instance any time from the **[Cloud Console](https://app.falkordb.cloud)**.

— The FalkorDB Team

---

*You're receiving this because you recently deleted a database on FalkorDB Cloud. You can reply to opt out of future check-ins.*

---

## Implementation notes

- **Send from a real person's address** (e.g., founder or DevRel), not `noreply@`. Reply rate roughly doubles on this kind of message when it looks personal.
- **Plain-text version required** — the HTML variant with the Grafana screenshot should always ship with a plain-text alternative listing the same numbers.
- **Variant A image fallback:** if `{grafana_screenshot_url}` is null at send time, drop the image block entirely and keep the numeric summary inline — don't ship a broken image icon.
- **Tracking:** tag replies with `deletion-followup-v1` and bucket by reason category so we can report monthly on top deletion drivers.
