# New Registrants Education Flow

> **Status:** 🟢 Proposed, for review. Replaces the [legacy flow](legacy-flow.md).

**Audience:** every new registrant in HubSpot. We send this before we know whether the contact created a FalkorDB database.

**Purpose:** customer success education. Help the contact start a free trial, find the docs, and run a first query. No sales push.

**Cadence:** Day 1. Then Day 3 if no reply. Then Day 6 if no reply.

**HubSpot source of truth:** [registration sequence](https://app-eu1.hubspot.com/sequences/144055056/sequence/248070596/edit?page=2)

**Why three steps:** the database aware journeys (Free, Paid, Churn) pick up after this flow. This generic flow stays short and ends before those journeys start.

---

## Conventions for this flow

- We do not use a first name greeting token. The greeting stays generic.
- We do not include pricing or Enterprise links in this flow.
- Wording follows the house style. No dash punctuation. Few commas. Short sentences.

---

## Step 1 (Day 1): Welcome

**Goal:** welcome the contact. Point them to the free trial. Give the fastest path to a first query.

**Subject:** Welcome to FalkorDB. Start your free trial.

Welcome to FalkorDB. FalkorDB Cloud is your fully managed graph database. It is built for ultra-low latency and a small memory footprint. We handle scale, security, and operations so you can focus on building.

**What's next**

1. **Start with a free trial.** Spin up a free FalkorDB instance in a couple of minutes at no cost. Move up to a dedicated instance when you are ready for testing, prototypes, or production.
2. **Connect your way.** Open the built-in Browser UI to start querying right away. You can also copy your connection details from the Connectivity tab and connect from any official FalkorDB client library.
3. **Run your first query.** Follow the quick walkthrough to build your first graph and run your first Cypher query. Most teams get there in about 10 minutes.

**Start your free trial:** <https://app.falkordb.cloud/signin>

**Build faster with these resources**

- **Explore visually.** Query and inspect your graph in the FalkorDB Browser UI: <https://docs.falkordb.com/browser/>
- **Learn the graph model.** See how nodes, labels, relationships, and paths fit together in the labeled property graph: <https://docs.falkordb.com/datatypes.html>
- **Coming from SQL?** See how relational concepts map to Cypher: <https://docs.falkordb.com/cypher/>
- **Build your knowledge graph.** Turn raw documents into cited, AI-ready answers with GraphRAG: <https://docs.falkordb.com/genai-tools/graphrag-sdk>
- **Level up.** Short getting-started guides for your first graph and first query: <https://docs.falkordb.com/getting-started/>

**Take me to the docs:** <https://docs.falkordb.com/getting-started/>

Regards,

The FalkorDB Team

---

## Step 2 (Day 3, if no reply): See what teams build

**Goal:** show what FalkorDB customers build with graphs, with proof points and links. Use cases only.

**Subject:** See what teams build on FalkorDB

From fraud detection to network monitoring to identity systems, teams use the FalkorDB graph engine to power real time, connected applications. They pick FalkorDB for speed at scale. See the benchmarks: <https://benchmark.falkordb.com/>

**Start your free trial:** <https://app.falkordb.cloud/signin>

**What FalkorDB customers build**

- **Detecting fraud in real time.** A large payments processor surfaces fraud rings across IPs, devices, and transactions in real time. See the security case study: <https://www.falkordb.com/case-studies/securin-falkordb-graph-case-study/>
- **Mapping network topology.** A Fortune 500 network provider models more than 60,000 topology graphs for live monitoring across US, EU, and SG.
- **Powering identity and access.** A phone manufacturer manages dynamic roles, groups, and hierarchies on a 300 GB cluster, tracing users, roles, and assets for real time authorization and to pinpoint access vulnerabilities.
- **Observing Kubernetes.** An observability platform turns Kubernetes metrics into a live knowledge graph for topology, contextual alerting, and fast search.

**See all use cases:** <https://www.falkordb.com/use-cases/>

Regards,

The FalkorDB Team

---

## Step 3 (Day 6, if no reply): What you can build

**Goal:** show a few common use cases. Close the series politely. Leave one resource list.

**Subject:** What teams build on FalkorDB

Thanks for spending the week with FalkorDB. This is the last email in this short series. Teams use FalkorDB for many graph workloads.

- **GraphRAG and AI.** Knowledge-graph-backed RAG with the GraphRAG SDK.
- **Knowledge graphs.** Connect entities, concepts, and facts for search, chatbots, and discovery.
- **Recommendations.** Personalized feeds and "customers who bought X also bought Y".
- **Fraud detection.** Surface fraud rings by shared devices, phones, addresses, and IPs.
- **Infrastructure mapping.** Blast radius and dependency analysis for services and databases.
- **Supply chain.** Model suppliers, products, warehouses, and single-source-of-supply risk.

**All your resources in one place**

- Cloud console: <https://app.falkordb.cloud/signin>
- Documentation: <https://docs.falkordb.com/>
- Cypher reference: <https://docs.falkordb.com/cypher/>
- Client libraries: <https://docs.falkordb.com/getting-started/clients.html>
- Browser UI: <https://docs.falkordb.com/browser/>
- GraphRAG SDK: <https://docs.falkordb.com/genai-tools/graphrag-sdk>
- Community discussions: <https://github.com/orgs/FalkorDB/discussions>
- Discord: <https://discord.gg/AEHAVvH5GU>

No need to reply unless we can help with something specific.

Regards,

The FalkorDB Team

---

## After this flow

Contacts move into the database aware journeys (Free DB, Paid DB, Churn) based on what happens in their account.
