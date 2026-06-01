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

## Proposed CS-oriented replacement flow (A/B test, for review)

The current 4-step sales-flavored sequence is replaced with a **3-step CS-oriented flow** that we test as two parallel paths. Cadence is identical across paths so we can isolate the effect of the messaging strategy.

**Cadence (both paths):** Day 1 → Day 3 (if no reply) → Day 6 (if no reply).

**Why 3 steps:** subsequent journeys (Free DB creation, Paid DB) will pick up engagement from here, so this generic flow should stay short and end before the user-specific journeys start.

### Test design

| | Path A — Education | Path B — Use case |
|---|---|---|
| **Hypothesis** | Contacts activate faster when given a clear, low-pressure path to docs and Cloud setup. | Contacts engage more when they see concrete things they can build with FalkorDB. |
| **Audience split** | 50% | 50% |
| **Primary metric** | Clicks to docs / Cloud console | Clicks to use-case docs (GraphRAG, Knowledge Graph, Recommendations, Fraud, Infra, Supply Chain) |
| **Secondary metrics** | DB creation, replies, Cloud-pricing-page clicks, Enterprise-link clicks | DB creation, replies, Cloud-pricing-page clicks, Enterprise-link clicks |
| **Tone** | Customer success, documentation-first, low-pressure | Customer success, discovery-driven, "here's what you can build" |
| **Shared elements (both paths)** | Cloud pricing link, Enterprise deployment link, support/community links at the bottom of every email |

**Shared placeholders to confirm before launch:**

- `{Cloud pricing link}` — final FalkorDB Cloud pricing page URL.
- `{Enterprise deployment link}` — Enterprise deployment / contact path.
- `{First Name}` — HubSpot personalization token to confirm.

---

## Path A — Education

CS-led, documentation-first. Each step links to getting-started content and self-serve resources, with Cloud pricing and Enterprise deployment always visible.

### Path A — Step 1 — Day 1

**Goal:** welcome the contact and give them the fastest path to self-serve setup.

**Subject:** Getting started with FalkorDB

Hi {First Name},

Welcome to FalkorDB. Here are the fastest links to get started:

1. **Open the FalkorDB Cloud console:** <https://app.falkordb.cloud/signin>
2. **Cloud getting started guide:** <https://docs.falkordb.com/cloud>
3. **Build your first graph (10 min walkthrough):** <https://docs.falkordb.com/getting-started/>
4. **Browser UI — visualize and query your graph:** <https://docs.falkordb.com/browser/>
5. **Cypher cheat sheet:** <https://docs.falkordb.com/cypher/>

Want to compare plans? **Cloud plans and pricing:** {Cloud pricing link}.

Need a dedicated or self-hosted setup? **Enterprise deployment:** {Enterprise deployment link}.

Regards,

The FalkorDB Team

---

### Path A — Step 2 — Day 3 (if no reply)

**Goal:** help contacts who have not replied move from "signed up" to "first query," without pressure.

**Subject:** A short FalkorDB setup checklist

Hi {First Name},

If you're still getting set up, here's a short checklist that takes most teams under 15 minutes end-to-end:

1. Sign in to the Cloud console.
2. Create a database (Free tier is fine to start).
3. Connect using a client library (Python, Node.js, Java, Go, Rust, C#, PHP).
4. Run your first Cypher query.
5. Explore the graph in the built-in browser UI — see the **[Browser UI docs](https://docs.falkordb.com/browser/)**.

Helpful docs:

- **Client libraries quick start:** <https://docs.falkordb.com/getting-started/clients.html>
- **Data modeling guide:** <https://docs.falkordb.com/>
- **Indexing & performance tips:** <https://docs.falkordb.com/>

**Cloud plans and pricing:** {Cloud pricing link} · **Enterprise deployment:** {Enterprise deployment link}

Regards,

The FalkorDB Team

---

### Path A — Step 3 — Day 6 (if no reply)

**Goal:** close the generic education flow politely and leave one consolidated resource list. After this email, contacts continue in the appropriate DB-aware journey (Free or Paid).

**Subject:** FalkorDB resources in one place

Hi {First Name},

This is the last email in this short getting-started series. All the FalkorDB resources you may need are below:

- **Cloud console:** <https://app.falkordb.cloud/signin>
- **Documentation:** <https://docs.falkordb.com/>
- **Cypher reference:** <https://docs.falkordb.com/cypher/>
- **Client libraries:** <https://docs.falkordb.com/getting-started/clients.html>
- **Browser UI:** <https://docs.falkordb.com/browser/>
- **GraphRAG SDK:** <https://docs.falkordb.com/genai-tools/graphrag-sdk>
- **Cloud plans and pricing:** {Cloud pricing link}
- **Enterprise deployment:** {Enterprise deployment link}
- **Community discussions:** <https://github.com/orgs/FalkorDB/discussions>
- **Discord:** <https://discord.gg/AEHAVvH5GU>

No need to reply unless we can help with something specific.

Regards,

The FalkorDB Team

---

## Path B — Use case

CS-led, discovery-driven. Step 1 still teaches getting started, but anchors it in *what the contact could build*. Steps 2 and 3 expand on those use cases — Step 2 covers AI/GraphRAG use cases, Step 3 covers operational/data use cases.

### Path B — Step 1 — Day 1

**Goal:** welcome the contact, show them how to get started, and give a one-line snapshot of the kinds of things teams build on FalkorDB.

**Subject:** Welcome to FalkorDB — here's what you can build

Hi {First Name},

Welcome to FalkorDB. Two quick things to start with:

**1. Get set up in a few minutes:**

- **FalkorDB Cloud console:** <https://app.falkordb.cloud/signin>
- **Cloud getting started guide:** <https://docs.falkordb.com/cloud>
- **Build your first graph:** <https://docs.falkordb.com/getting-started/>
- **Browser UI — visualize and query your graph:** <https://docs.falkordb.com/browser/>

**2. What you can build on FalkorDB:**

- **GraphRAG / AI applications** — knowledge-graph-backed RAG with the GraphRAG SDK.
- **Knowledge graphs** — connect entities, concepts, and facts for search, chatbots, and discovery.
- **Recommendations** — "customers who bought X also bought Y," personalized feeds.
- **Fraud detection** — surface fraud rings by shared devices, phones, addresses, IPs.
- **IT infrastructure / dependency mapping** — blast-radius and impact analysis.
- **Supply chain** — suppliers, products, warehouses, single-source risk.

Over the next couple of emails we'll go deeper into the use cases above.

**Cloud plans and pricing:** {Cloud pricing link} · **Enterprise deployment:** {Enterprise deployment link}

Regards,

The FalkorDB Team

---

### Path B — Step 2 — Day 3 (if no reply)

**Goal:** deepen the use-case story for AI / GraphRAG / knowledge graph builders, since this is FalkorDB's most differentiated use case.

**Subject:** Building AI and knowledge graphs on FalkorDB

Hi {First Name},

If you're building AI-powered applications, FalkorDB is designed for it:

- **GraphRAG SDK** — turn user questions into Cypher queries automatically, with OpenAI, Gemini, or Groq. Docs: <https://docs.falkordb.com/genai-tools/graphrag-sdk>
- **Knowledge graphs** — connect entities, concepts, and facts to give LLMs richer, less hallucination-prone context.
- **Multi-tenant by default** — built-in multi-tenant capabilities for assistant / chatbot products.
- **Multi-agent workflows** — orchestrate ingestion and reasoning across multiple agents using the GraphRAG SDK.

If you're not building with AI, the next email covers more operational use cases (recommendations, fraud, infrastructure, supply chain).

**Cloud plans and pricing:** {Cloud pricing link} · **Enterprise deployment:** {Enterprise deployment link}

Regards,

The FalkorDB Team

---

### Path B — Step 3 — Day 6 (if no reply)

**Goal:** cover the remaining operational/data use cases for contacts who didn't engage with the AI/GraphRAG angle, then politely close the flow.

**Subject:** Recommendations, fraud, infrastructure, supply chain on FalkorDB

Hi {First Name},

FalkorDB is a fit for several operational graph workloads. A few patterns teams use most:

- **Recommendation engines** — collaborative filtering ("customers who bought X also bought Y") and personalized recommendations through shared user/product graphs.
- **Fraud detection** — find fraud rings by shared devices, phone numbers, addresses, or IPs; detect suspicious clusters that are invisible in tabular data.
- **IT infrastructure / dependency mapping** — impact analysis, blast radius, dependency chains for services and databases.
- **Supply chain** — model suppliers, products, warehouses, and single-source-of-supply risk.

If any of these match what you're building, our docs are the best starting point: <https://docs.falkordb.com/>

This is the last email in this short series. After this, you'll only hear from us based on what happens in your account.

**Cloud plans and pricing:** {Cloud pricing link} · **Enterprise deployment:** {Enterprise deployment link}

Regards,

The FalkorDB Team

---

## A/B test next steps (operational)

1. Confirm the Cloud pricing URL and Enterprise deployment link before launch.
2. Set the HubSpot personalization token for `{First Name}`.
3. Split the registrants list 50/50 between Path A and Path B in HubSpot.
4. Run the test for at least 4 weeks (or until ~1,000 contacts per arm).
5. Compare on primary metric first, then on DB-creation rate.
6. The winning path becomes the default; the losing path remains documented here for reference.
7. After this flow, contacts move into the **Free DB Creation** or **Paid DB** journeys (designed next).
