# New Registrants — Legacy Flow (As-Is in HubSpot)

> **Status:** 🟠 **Legacy** — this is the sequence currently running in HubSpot for new registrants. It is planned for replacement by the new 3-step A/B test ([Path A](path-a-education.md) / [Path B](path-b-use-case.md)). Documented here for reference and so we know what we're replacing.

**Audience:** new HubSpot contacts in the registration / pending-registration list. Database ownership/activity is unknown at this stage.

**HubSpot source of truth:** [registration sequence](https://app-eu1.hubspot.com/sequences/144055056/sequence/248070596/edit?page=2)

**Review direction:** the current HubSpot copy is sales-heavy ("30 min meeting" CTA on every step). The new flow rewrites this to be CS-led, documentation-first, and short.

---

## Sequence steps documented so far

| Step | Timing | HubSpot action | Audience / label | A/B test | Version | Status |
|---|---|---|---|---|---|---|
| 1 | Day 1 | Automated Email | Registrants - First email | No active B version | A only | Documented |
| 2 | Day 3 if no reply | Automated Email | Registrants - second email | No active B version | A only | Documented |
| 3 | Day 6 if no reply | Automated Email | Registrants - Third email | No active B version | A only | Documented |
| 4 | Day 9 if no reply | Automated Email | Registrants - fourth email | No active B version | A only | Documented |

---

## Step 1 — Automated Email — Day 1

**HubSpot label:** Registrants - First email

**A/B test:** no active Version B. HubSpot may have shown the option to add an A/B test, but only Version A exists today.

**Version documented:** Version A (only existing version)

**Subject:** Welcome to FalkorDB! Let's Get You Started

### Email body

Hi {First Name},

Welcome to FalkorDB! We're excited to have you join our community! FalkorDB is here to help you manage and analyze your graph data with ease and efficiency.

Here's how to get started:

1. **Log in:** Visit <https://app.falkordb.cloud/signin> and use your credentials to access your dashboard.
2. **Explore our resources:** Check out our documentation to get familiar with FalkorDB capabilities.
3. **Graph RAG:** GraphRAG SDK is here to support you with building a multi-tenant and multi-agent RAG application.

If you have any questions, feel free to reach out by replying to this email or using the following channels:

- **Email:** support@falkordb.com
- **Discord:** <https://discord.gg/AEHAVvH5GU>
- **Forum:** <https://github.com/orgs/FalkorDB/discussions>

We are interested to learn more about your use case. Will be glad to chat: 30 min meeting.

Thanks,

The FalkorDB Team

---

## Step 2 — Automated Email — Day 3

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

## Step 3 — Automated Email — Day 6

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

## Step 4 — Automated Email — Day 9

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
- Remaining sequence steps after Day 9 still need to be documented (if any exist beyond the four above).
- Final Cloud pricing URL should be confirmed.
- Final Enterprise deployment CTA/link should be confirmed.
