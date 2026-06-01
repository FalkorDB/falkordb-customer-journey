# New Registrants — Generic Education Flow

This directory documents the journey for **new registrants** in HubSpot: contacts that have just registered (or are pending registration) and for whom we do **not** yet know whether they created a FalkorDB database.

**Audience:** every new HubSpot contact entering the registration / pending-registration list. No database ownership or activity signal is available at this stage.

**Purpose:** generic, customer-success-led education — get the contact set up, point them at the docs and the Cloud console, and surface pricing / Enterprise options. This is *not* a database-activation journey; DB-aware journeys (Free, Paid, Churn) pick up after this flow.

**HubSpot source of truth:** [registration sequence](https://app-eu1.hubspot.com/sequences/144055056/sequence/248070596/edit?page=2)

---

## Files in this folder

| File | What it is | Status |
|---|---|---|
| [`legacy-flow.md`](legacy-flow.md) | The current HubSpot 4-step sequence (Days 1 / 3 / 6 / 9), all Version A only. Sales-flavored. | 🟠 Legacy — active in HubSpot today, planned for replacement |
| [`path-a-education.md`](path-a-education.md) | **New flow, Path A — Education.** 3 steps (Days 1 / 3 / 6), CS-led, documentation-first. Each step has Version A and Version B for email-level A/B testing. | 🟢 New — proposed, for review |
| [`path-b-use-case.md`](path-b-use-case.md) | **New flow, Path B — Use case.** 3 steps (Days 1 / 3 / 6), CS-led, use-case-focused. One version per step (no within-step A/B). | 🟢 New — proposed, for review |

---

## New flow — A/B test design

The legacy 4-step sales-flavored sequence is being replaced with a **3-step CS-oriented flow** that runs as two parallel paths to test the messaging strategy.

**Cadence (both paths):** Day 1 → Day 3 (if no reply) → Day 6 (if no reply).

**Why 3 steps:** subsequent journeys (Free DB creation, Paid DB) will pick up engagement from here, so this generic flow should stay short and end before the user-specific journeys start.

### Test design

| | Path A — Education | Path B — Use case |
|---|---|---|
| **Hypothesis** | Contacts activate faster when given a clear, low-pressure path to docs and Cloud setup. | Contacts engage more when they see concrete things they can build with FalkorDB. |
| **Audience split** | 50% of new registrants | 50% of new registrants |
| **Primary metric** | Clicks to docs / Cloud console | Clicks to use-case docs (GraphRAG, Knowledge Graph, Recommendations, Fraud, Infra, Supply Chain) |
| **Secondary metrics** | DB creation, replies, Cloud-pricing-page clicks, Enterprise-link clicks | DB creation, replies, Cloud-pricing-page clicks, Enterprise-link clicks |
| **Tone** | Customer success, documentation-first, low-pressure, no sales push | Customer success, discovery-driven, "here's what you can build", no sales push |
| **Shared elements (both paths)** | Educational getting-started links in every email. Cloud pricing shown as an informational link from Day 1; Enterprise deployment link only appears in the later steps (kept out of the Day 1 welcome to avoid a sales tone). |

### Two layers of A/B testing

1. **Path-level (A vs B):** Education vs Use case framing — 50/50 audience split.
2. **Email-level (Version A vs Version B), Path A only:** each Path A step has two HubSpot variants so we can also test subject line / copy style with the path held fixed. Pick one winner per step before promoting the path. **Path B runs a single version per step** and is compared at the path level only.

### Shared placeholders to confirm before launch

- `{Cloud pricing link}` — final FalkorDB Cloud pricing page URL.
- `{Enterprise deployment link}` — Enterprise deployment / contact path.
- `{First Name}` — HubSpot personalization token to confirm.

---

## Operational next steps

1. Confirm the Cloud pricing URL and Enterprise deployment link before launch.
2. Set the HubSpot personalization token for `{First Name}`.
3. Split the new-registrants list 50/50 between Path A and Path B in HubSpot.
4. Run the test for at least 4 weeks (or until ~1,000 contacts per arm).
5. Compare on primary metric first, then on DB-creation rate.
6. The winning path becomes the default; the losing path stays documented here for reference.
7. After this flow, contacts move into the **Free DB Creation** or **Paid DB** journeys (designed next).
