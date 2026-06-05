# Current All-Contact Education Flow (As-Is)

This file documents the current HubSpot registration / pending-registration sequence as it exists today.
This is a generic education flow sent to contacts before we know whether they have created any FalkorDB database.

**Source of truth:** [HubSpot registration journey](https://app-eu1.hubspot.com/sequences/144055056/sequence/248070596/edit?page=2)

**Audience:** contacts registered in HubSpot and pending registration. Database ownership/activity is unknown at this stage.

**Purpose:** customer-success education: help contacts understand how to get started, where to find documentation, what FalkorDB Cloud offers, and where Enterprise deployment information will live.

**Status:** active.

**Review direction:** the current HubSpot copy is sales-heavy. Proposed replacement copy is included below for review and should stay short, helpful, and documentation-first.

---

## Sequence steps documented so far

| Step | Timing | HubSpot action | Audience / label | A/B test | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Day 1 | Automated Email | Registrants - First email | No active B version | A only | Documented |
| 2 | Day 3 if no reply | Automated Email | Registrants - second email | No active B version | A only | Documented |
| 3 | Day 6 if no reply | Automated Email | Registrants - Third email | No active B version | A only | Documented |
| 4 | Day 9 if no reply | Automated Email | Registrants - fourth email | No active B version | A only | Documented |

---

## Step 1 — Automated Email - Day 1

**HubSpot label:** Registrants - First email

**A/B test:** no active Version B. HubSpot may have shown the option to add an A/B test, but only Version A exists today.

**Version documented:** Version A (CS-oriented replacement applied)

**Rendered HTML email:** registrants receive the designed HTML version in [`journeys/templates/welcome-day1.html`](templates/welcome-day1.html). The Markdown copy below is the source of truth for wording; the HTML file is the visual layout (FalkorDB-branded, modeled on the MongoDB Atlas welcome email).

**Subject:** Getting started with FalkorDB Cloud

### Email body

Hi {First Name},

Welcome to FalkorDB. If you're evaluating FalkorDB Cloud, these are the best places to start:

1. **Create or open your Cloud instance:** <https://app.falkordb.cloud/signin>
2. **Follow the getting-started guide:** <https://docs.falkordb.com/cloud>
3. **Build your first graph:** <https://docs.falkordb.com/getting-started/>

You can also review Cloud plans and pricing here: {Cloud pricing link}.

If your team needs a dedicated or Enterprise deployment, we'll add that path here: {Enterprise deployment link}.

Regards,

The FalkorDB Team

### QA checklist (verify before sending)

Run through this before pushing the HTML email live in HubSpot:

**Rendering**

- [ ] Renders correctly in Gmail (web + mobile app), Outlook, and Apple Mail.
- [ ] Responsive layout collapses cleanly on a narrow mobile viewport (≤ 600px).
- [ ] Brand purple header gradient and CTA buttons display (check Outlook VML fallback).
- [ ] Resource and social icons load and are tinted to the FalkorDB purple (`#7466FF`).
- [ ] `{First Name}` personalization token resolves (no literal `{First Name}` in the sent email).

**Links (every URL clicks through to the right place)**

- [ ] Primary CTA "Get started" → <https://app.falkordb.cloud/signin>
- [ ] Secondary CTA "Take me to the docs" → <https://docs.falkordb.com/getting-started/>
- [ ] Getting-started guide → <https://docs.falkordb.com/cloud>
- [ ] Build your first graph → <https://docs.falkordb.com/getting-started/>
- [ ] Discord → <https://discord.gg/AEHAVvH5GU>
- [ ] YouTube → <https://www.youtube.com/@FalkorDB>
- [ ] LinkedIn → <https://www.linkedin.com/company/falkordb>
- [ ] X → <https://x.com/falkordb>
- [ ] `{Cloud pricing link}` placeholder replaced with the final URL.
- [ ] `{Enterprise deployment link}` placeholder replaced with the final URL.
- [ ] Footer "View in browser" and "Unsubscribe" links wired up.

**Content**

- [ ] Subject line matches the documented copy.
- [ ] No leftover sales-tone phrasing (documentation-first).
- [ ] Sent a test email to an internal inbox and visually confirmed.

---

## Step 2 — Automated Email - Day 3

**Send condition:** if no reply after the Day 1 email.

**HubSpot label:** Registrants - second email

**Threading:** new thread.

**A/B test:** no active Version B. HubSpot may have shown the option to add an A/B test, but only Version A exists today.

**Version documented:** Version A (only existing version)

**Subject:** Discover FalkorDB's Powerful Features

### Email body

Hi {First Name},

We hope you've started exploring FalkorDB. Here are some powerful features that can help you get the most out of our platform:

1. **Graph Algorithms:** Leverage graph algorithms to uncover insights in your data.
2. **Cypher Query Language:** Use Cypher, the powerful query language, to manipulate and analyze your data with ease.
3. **Visual Data Representation:** Visualize your data with our visualization tool for better understanding and communication.

Have questions? Let's schedule a call to discuss: 30 min meeting.

Regards,

The FalkorDB Team

---

## Step 3 — Automated Email - Day 6

**Send condition:** if no reply after the Day 3 email; sent after another 3 business days.

**HubSpot label:** Registrants - Third email

**Threading:** new thread.

**A/B test:** no active Version B. HubSpot may have shown the option to add an A/B test, but only Version A exists today.

**Version documented:** Version A (only existing version)

**Subject:** FalkorDB is perfect to improve your RAG!

**Current HubSpot performance:**

| Sends | Opens | Clicks | Replies | Meetings |
|---:|---:|---:|---:|---:|
| 3,667 | 38% | 4% | 0% | 1% |

### Email body

Hi {First Name},

We hope you're finding FalkorDB valuable for your data management and analysis needs. Today, we want to introduce you to a powerful use case: Graph RAG.

1. **Graph RAG:** The ultra-low latency functionality of FalkorDB makes it a perfect infrastructure for building a knowledge graph for RAG applications.
2. **Built-in Multi-Tenancy:** FalkorDB provides the out-of-the-box multi-tenant capabilities to support personal assistant / chatbot use cases.
3. **Multi-Agent Workflows:** Multi-agent workflows can be created with the help of the GraphRAG SDK that you can use to ingest data and orchestrate the entire multi-agent flow.

Tell us more about your use case and we will be happy to assist: 30 min meeting.

Regards,

The FalkorDB Team

---

## Step 4 — Automated Email - Day 9

**Send condition:** if no reply after the Day 6 email; sent after another 3 business days.

**HubSpot label:** Registrants - fourth email.

**Threading:** new thread.

**A/B test:** no active Version B. HubSpot may have shown the option to add an A/B test, but only Version A exists today.

**Version documented:** Version A (only existing version)

**Subject:** Have you given up on FalkorDB???

### Email body

{First Name},

Last try :) Will be glad to discuss how we can be of benefit to your team.

Regards,

The FalkorDB Team

---

## Notes / gaps to capture

- The exact HubSpot personalization token for the greeting should be confirmed.
- The "30 min meeting" link / CTA target should be captured if it exists in HubSpot.
- Remaining sequence steps after Day 9 still need to be documented.
- Final Cloud pricing URL should be confirmed.
- Final Enterprise deployment CTA/link should be confirmed.

---

## Proposed CS-oriented replacement flow (for review)

This proposed version keeps the same rough cadence but changes the tone from sales follow-up to customer-success education.

### Proposed Step 2 — Day 3

**Goal:** help contacts who have not replied find the key setup docs without pressure.

**Subject:** FalkorDB Cloud setup checklist

Hi {First Name},

Here is a short checklist for getting started with FalkorDB Cloud:

1. Sign in to the Cloud console.
2. Create a database or open an existing one.
3. Connect using a client library.
4. Run your first Cypher query.
5. Use the browser UI to inspect and explore your graph.

Helpful docs:

- Cloud getting started: <https://docs.falkordb.com/cloud>
- Client libraries: <https://docs.falkordb.com/getting-started/clients.html>
- Cypher reference: <https://docs.falkordb.com/cypher/>

Regards,

The FalkorDB Team

---

### Proposed Step 3 — Day 6

**Goal:** introduce common use cases, especially GraphRAG, without assuming the contact has started building.

**Subject:** Common ways teams use FalkorDB

Hi {First Name},

FalkorDB is commonly used for knowledge graphs, recommendations, fraud detection, infrastructure mapping, and GraphRAG applications.

If you're exploring GraphRAG, start here:

- GraphRAG SDK docs: <https://docs.falkordb.com/genai-tools/graphrag-sdk>
- FalkorDB use cases: <https://docs.falkordb.com/>

For Cloud, you can compare available options here: {Cloud pricing link}. For Enterprise deployment, use this path: {Enterprise deployment link}.

Regards,

The FalkorDB Team

---

### Proposed Step 4 — Day 9

**Goal:** close the generic education flow politely and leave useful links.

**Subject:** FalkorDB resources in one place

Hi {First Name},

This is the last email in this short getting-started series. Here are the main FalkorDB resources in one place:

- Cloud console: <https://app.falkordb.cloud/signin>
- Documentation: <https://docs.falkordb.com/>
- Cloud plans and pricing: {Cloud pricing link}
- Enterprise deployment: {Enterprise deployment link}
- Community forum: <https://github.com/orgs/FalkorDB/discussions>

No need to reply unless we can help with something specific.

Regards,

The FalkorDB Team
