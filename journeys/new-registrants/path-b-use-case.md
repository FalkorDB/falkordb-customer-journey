# New Registrants — New Flow, Path B — Use Case

> **Status:** 🟢 **New — proposed, for review.** Replacement for the [legacy flow](legacy-flow.md). See the [folder README](README.md) for the overall A/B test design and shared placeholders.

**Audience:** 50% of **new registrants** in HubSpot (Path B arm of the path-level A/B test).

**Framing:** CS-led, discovery-driven. Step 1 still teaches getting started, but anchors it in *what the contact could build*. Steps 2 and 3 expand on those use cases — Step 2 covers AI/GraphRAG use cases, Step 3 covers operational/data use cases.

**Cadence:** Day 1 → Day 3 (if no reply) → Day 6 (if no reply).

**Within-step A/B:** every step has a **Version A** and **Version B** so HubSpot can also test subject line / copy style with the path held fixed.

---

## Path B — Step 1 — Day 1

**Goal:** welcome the contact, show them how to get started, and give a one-line snapshot of the kinds of things teams build on FalkorDB.

### Version A — "Welcome + what you can build" (broad menu)

**Subject:** Welcome to FalkorDB — here's what you can build

Hi {First Name},

Welcome to FalkorDB! We're excited to have you join our community and can't wait to see what you build with us. Two quick things to start with:

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

### Version B — "What are you building?" (discovery question framing)

**Subject:** What are you building on FalkorDB?

Hi {First Name},

Welcome to FalkorDB — really happy to have you here! Quick question to make sure we point you in the right direction: **what are you trying to build?**

Most teams arrive here for one of these:

- **AI / GraphRAG** — give your LLM a knowledge graph so answers are grounded and traceable.
- **Recommendations** — model users, products, and behavior as a graph.
- **Fraud / risk** — find rings and clusters that tabular data hides.
- **IT / network / supply chain** — model dependencies and run impact analysis.

Reply with one line about your use case and we'll point you straight at the most relevant docs and examples.

While you wait, get set up in a few minutes:

- **Cloud console:** <https://app.falkordb.cloud/signin>
- **First graph in 10 minutes:** <https://docs.falkordb.com/getting-started/>
- **Browser UI:** <https://docs.falkordb.com/browser/>

**Cloud plans and pricing:** {Cloud pricing link} · **Enterprise deployment:** {Enterprise deployment link}

Regards,

The FalkorDB Team

---

## Path B — Step 2 — Day 3 (if no reply)

**Goal:** deepen the use-case story for AI / GraphRAG / knowledge graph builders, since this is FalkorDB's most differentiated use case.

### Version A — "Building AI on FalkorDB" (capability list)

**Subject:** Building AI and knowledge graphs on FalkorDB

Hi {First Name},

Hope you're enjoying exploring FalkorDB! If you're building AI-powered applications, FalkorDB is designed for it:

- **GraphRAG SDK** — turn user questions into Cypher queries automatically, with OpenAI, Gemini, or Groq. Docs: <https://docs.falkordb.com/genai-tools/graphrag-sdk>
- **Knowledge graphs** — connect entities, concepts, and facts to give LLMs richer, less hallucination-prone context.
- **Multi-tenant by default** — built-in multi-tenant capabilities for assistant / chatbot products.
- **Multi-agent workflows** — orchestrate ingestion and reasoning across multiple agents using the GraphRAG SDK.

If you're not building with AI, the next email covers more operational use cases (recommendations, fraud, infrastructure, supply chain).

**Cloud plans and pricing:** {Cloud pricing link} · **Enterprise deployment:** {Enterprise deployment link}

Regards,

The FalkorDB Team

### Version B — "Why graphs for RAG" (problem-first framing)

**Subject:** Why your RAG keeps hallucinating — and what a graph fixes

Hi {First Name},

Glad to have you building with FalkorDB! Quick thought if you're working on RAG: vector-only RAG is great at finding *similar* text, but not great at answering questions that need to *connect* facts ("which of our customers in the EU use feature X and have an open support ticket?").

That's where a graph helps:

- **Structure the relationships, not just the embeddings** — entities, facts, and how they connect.
- **Ground the LLM in traceable answers** — every claim is backed by a path in the graph.
- **Built-in multi-tenancy** — give each user/tenant their own graph without standing up new infra.
- **Multi-agent orchestration** with the **GraphRAG SDK** — ingest, reason, answer.

Start here: <https://docs.falkordb.com/genai-tools/graphrag-sdk>

Next email covers non-AI use cases (recommendations, fraud, infrastructure, supply chain) if those are closer to what you're building.

**Cloud plans and pricing:** {Cloud pricing link} · **Enterprise deployment:** {Enterprise deployment link}

Regards,

The FalkorDB Team

---

## Path B — Step 3 — Day 6 (if no reply)

**Goal:** cover the remaining operational/data use cases for contacts who didn't engage with the AI/GraphRAG angle, then politely close the flow.

### Version A — "Operational graph workloads" (capability list)

**Subject:** Recommendations, fraud, infrastructure, supply chain on FalkorDB

Hi {First Name},

Thanks for sticking with us through this short series! FalkorDB is a fit for several operational graph workloads — a few patterns teams use most:

- **Recommendation engines** — collaborative filtering ("customers who bought X also bought Y") and personalized recommendations through shared user/product graphs.
- **Fraud detection** — find fraud rings by shared devices, phone numbers, addresses, or IPs; detect suspicious clusters that are invisible in tabular data.
- **IT infrastructure / dependency mapping** — impact analysis, blast radius, dependency chains for services and databases.
- **Supply chain** — model suppliers, products, warehouses, and single-source-of-supply risk.

If any of these match what you're building, our docs are the best starting point: <https://docs.falkordb.com/>

This is the last email in this short series. After this, you'll only hear from us based on what happens in your account.

**Cloud plans and pricing:** {Cloud pricing link} · **Enterprise deployment:** {Enterprise deployment link}

Regards,

The FalkorDB Team

### Version B — "Pick the pattern closest to yours" (pick-one framing)

**Subject:** Which of these looks closest to what you're building?

Hi {First Name},

Thanks for being part of the FalkorDB community! Quick way to wrap up this short series — pick the pattern closest to what you're building and dive in:

- **Recommendations** — users, products, and behavior modeled as a graph for collaborative filtering and personalization. → <https://docs.falkordb.com/>
- **Fraud / risk** — detect rings and shared-identity clusters that tabular queries miss. → <https://docs.falkordb.com/>
- **IT / network / dependencies** — blast radius, impact analysis, and runbook automation. → <https://docs.falkordb.com/>
- **Supply chain** — suppliers, products, warehouses, and single-source-of-supply risk. → <https://docs.falkordb.com/>

This is the last email in this short series. From here, you'll only hear from us based on what happens in your account — or if you reply with a question.

**Cloud plans and pricing:** {Cloud pricing link} · **Enterprise deployment:** {Enterprise deployment link}

Regards,

The FalkorDB Team
