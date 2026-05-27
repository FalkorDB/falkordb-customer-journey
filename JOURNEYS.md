# FalkorDB Customer Journeys

This document is the master index of the customer journeys we are designing for FalkorDB users.
Each journey is summarized here at a high level; detailed maps live in their own files (added one-by-one) and will be linked from the table below.

> **Status legend:** 🟢 Active · 🟡 In design · ⚪ Planned · 🔵 TBD (scope to confirm)

---

## 1. Journey set

### Priority journeys (designing now)

| # | Journey | One-line description | Status | Detailed map |
|---|---|---|---|---|
| 1 | **Current Customer Journey (As-Is)** | The journey contacts go through today in HubSpot when they are registered / pending registration. Single track, no plan-based branching. Baseline for everything else. | 🟢 Active | [§2](#2-current-customer-journey-as-is--summary) |
| 2 | **All-User Journey (Common Core)** | The shared backbone every user sees regardless of plan — signup → first DB → first query → onboarding education → deletion follow-up. The trunk that the Free and Paid journeys branch off. | ⚪ Planned | _TBD_ |
| 3 | **Free User Journey** | Free-tier active path: activation, education, nudges toward a real workload, upgrade triggers when bumping into Free limits, re-engagement when going cold. | ⚪ Planned | _TBD_ |
| 4 | **Paid User Journey** | Paid-tier active path: production readiness (replication, indexing, backups), expansion (more DBs, larger tiers, GraphRAG), health check-ins, renewal & retention, downgrade-risk handling. | ⚪ Planned | _TBD_ |
| 5 | **Free Churn Journey** ⭐ | A free user who had a free DB for **more than 2 weeks** and whose DB was then removed (by user or by system). Goal: understand *why*, attempt to recover them, and feed learnings back into product. | ⚪ Planned (top priority) | _TBD_ |
| 6 | **Paid Churn Journey** ⭐ | A paying customer who churned — subscription canceled, downgrade to free, or last paid DB removed. Goal: structured exit interview, save offer, and a multi-touch win-back path. | ⚪ Planned (top priority) | _TBD_ |

### Parking lot (scope to confirm later)

| # | Journey | Why it's TBD |
|---|---|---|
| 7 | **Trial Journey** 🔵 | Confirm whether FalkorDB Cloud will have an explicit trial concept distinct from Free tier. |
| 8 | **Self-hosted / OSS Journey** 🔵 | Different signal set (no account, GitHub/Docker-based). Confirm if/how we engage these users. |
| 9 | **Enterprise Journey** 🔵 | High-touch, sales-led, contract-driven. Confirm if this is part of the lifecycle program or owned fully by Sales/CS. |

---

## 2. Current Customer Journey (As-Is) — summary

**Current source of truth:** HubSpot sequence — [registration journey](https://app-eu1.hubspot.com/sequences/144055056/sequence/248070596/edit?page=2).

**Trigger:** contact is registered in HubSpot and enters the registration / pending-registration flow.

**Audience:** every HubSpot contact that matches the registration flow criteria.

| Step | When | Touchpoint | Source |
|---|---|---|---|
| 1 | Day 0 — on DB creation | Welcome + Onboarding | `messages/welcome_message_v1.md`, `messages/onboarding_message_v1.md` |
| 2 | Day 1–2 | Support handoff | `messages/support_contact_v1.md` |
| 3 | Day 3–5 | Tips & best practices | `messages/tips_best_practices_v1.md` |
| 4 | Event — first query | First-query celebration | `messages/first_query_celebration_v1.md` |
| 5 | Day 7+ (no activity) | Inactivity check-in | `messages/inactivity_checkin_v1.md` |
| 6 | Day 7–10 | GraphRAG introduction | `messages/graphrag_introduction_v1.md` |
| 7 | Day 14–21 (active users) | Feedback request | `messages/feedback_request_v1.md` |
| 8 | Day 30 (no login) | Churn prevention | `messages/churn_prevention_v1.md` |
| 9 | Event — DB deletion | Deletion follow-up (used / unused variants) | `messages/db_deletion_followup_v1.md`, `automation/deletion_followup/` |
| 10 | Usage-based — nearing limits | Upgrade / scale nudge | `messages/upgrade_scale_nudge_v1.md` |

**Observations / gaps:**
- No distinction between Free vs Paid — everyone receives the same sequence today.
- No explicit pre-signup / acquisition step.
- No "you just became paid" / post-upgrade moment.
- No renewal / expansion / win-back loop for paid users.
- Resources under `resources/*.md` exist but are not yet tied to specific journey steps.

---

## 3. Churn journeys — framing notes

These are the two priority journeys to design next. Below is the framing we'll expand into full maps.

### 3.1 Free Churn Journey ⭐

- **Trigger:** Free-tier DB existed **≥ 14 days**, then was deleted/removed (user-initiated *or* system-removed).
- **Sub-segmentation:**
  - User-initiated delete vs. system-removed (inactivity, quota, billing-related on free).
  - DB was *actively used* (had queries) vs. *empty / inactive*.
  - Hit a free-tier limit before deletion (Y / N).
- **Goals:** capture the *why*, offer a low-friction path back, surface product signal.
- **Mechanisms:** short exit survey (1–2 questions), behavioral signal capture, re-engagement sequence (preserved schema, "restore from backup", GraphRAG demo, etc.).

### 3.2 Paid Churn Journey ⭐

- **Trigger:** Paid subscription canceled **OR** last paid DB removed **OR** downgrade to Free.
- **Sub-segmentation by reason:** price, missing feature, performance, switched to competitor, project ended, team change, other.
- **Goals:** structured exit interview, save offer (pause / downgrade / discount where appropriate), multi-touch win-back.
- **Mechanisms:** higher-touch — human or async exit interview, save-offer flow, win-back cadence at 30d / 90d / 6mo with product-update digests.

---

## 4. How to use this document

1. This file is the index. Each journey gets its own detailed map in a follow-up file (e.g. `journeys/free-churn.md`) and is linked from the table in §1.
2. When a journey moves from 🟡 In design → 🟢 Active, update its status here.
3. When a new touchpoint is added under `messages/` or `automation/`, link it to the journey step(s) it belongs to.
