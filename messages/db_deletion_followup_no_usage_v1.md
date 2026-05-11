# DB Deletion Follow-Up — No Usage
**Trigger:** User deletes a FalkorDB Cloud database that had little or no activity
**Send timing:** Within 24 hours of deletion
**Tone:** Warm, low-pressure, curious — assume they barely got started, not that they failed
**Routing rule:** Deleted DB had **< 1,000 queries lifetime** AND **< 7 days of activity**

---

## Purpose

When a user spins up a Cloud database and tears it down without really trying
it, the most likely cause is friction in onboarding — not a deep product issue.
Ask one short question about what got in the way, and point them at the
guided First Graph walkthrough in case they want another go.

**Suppression:**
- Do **not** send if the user still has another active DB on the account.
- Do **not** send if the account itself was closed.
- Do **not** send if a deletion follow-up was already sent in the last 30 days.

---

## Tokens / data fields

Mostly minimal for this variant — there isn't much to report on. Useful tokens:

| Token | Source | Example |
|---|---|---|
| `{db_name}` | Cloud control plane | `test-graph-2` |
| `{First Name}` | CRM | `Alex` |

This variant intentionally does **not** include Grafana metrics or a
screenshot — there's nothing meaningful to show, and including empty/zero
numbers reads as passive-aggressive.

---

## Subject

Anything we could have done better?

---

## Body

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

- Send from a real person's address, same as the "with usage" variant.
- **Tracking:** tag replies with `deletion-followup-no-usage-v1` and bucket reasons (onboarding-friction / wrong-fit / docs / exploring / other) so we can prioritize onboarding fixes.
