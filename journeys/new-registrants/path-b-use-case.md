# New Registrants — New Flow, Path B — Use Case

> **Status:** 🟢 **New — proposed, for review.** Replacement for the [legacy flow](legacy-flow.md). See the [folder README](README.md) for the overall A/B test design and shared placeholders.

**Audience:** 50% of **new registrants** in HubSpot (Path B arm of the path-level A/B test).

**Framing:** CS-led, use-case-driven. Step 1 teaches getting started, but anchors it in *what the contact could build*. Steps 2 and 3 expand on those use cases — Step 2 covers AI/GraphRAG use cases, Step 3 covers operational/data use cases.

**Cadence:** Day 1 → Day 3 (if no reply) → Day 6 (if no reply).

**One version per step:** Path B is the use-case arm and runs a single version per step (no within-step A/B). The path-level A/B test is Path A (Education) vs Path B (Use case).

---

## Path B — Step 1 — Day 1

**Goal:** welcome the contact, gently encourage them to spin up a free database if they'd like, and give a snapshot of the kinds of things teams build on FalkorDB.

**Subject:** Welcome to FalkorDB — here's what you can build

Hi {First Name},

Welcome to FalkorDB! We're excited to have you join our community and can't wait to see what you build with us. Two quick things to start with:

**1. Get set up in a few minutes:**

The best way to get a feel for FalkorDB is to spin up a **free database** — it's free to try, takes a couple of minutes, and there's no pressure to do it right now.

- **Create your free database:** <https://app.falkordb.cloud/signin>
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

Want to learn about the Cloud tiers? Here's an overview: **Cloud plans and pricing:** {Cloud pricing link}

Regards,

The FalkorDB Team

---

## Path B — Step 2 — Day 3 (if no reply)

**Goal:** deepen the use-case story for AI / GraphRAG / knowledge graph builders, since this is FalkorDB's most differentiated use case.

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

---

## Path B — Step 3 — Day 6 (if no reply)

**Goal:** cover the remaining operational/data use cases for contacts who didn't engage with the AI/GraphRAG angle, then politely close the flow.

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
