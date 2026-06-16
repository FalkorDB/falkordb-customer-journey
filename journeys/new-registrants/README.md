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
- **Build identity management on a real time graph.**
  - Manage dynamic roles, groups, and hierarchies with a graph based IAM system.
  - Trace users, roles, and assets for real time authorization, and pinpoint vulnerabilities in complex access structures.
  - Proven at scale on a 300 GB cluster.
- **Observing Kubernetes.** An observability platform turns Kubernetes metrics into a live knowledge graph for topology, contextual alerting, and fast search.

**See all use cases:** <https://www.falkordb.com/use-cases/>

Regards,

The FalkorDB Team

---

## Step 3 (Day 6, if no reply): A few best practices

**Goal:** close the series with practical best practices that help new users build fast, reliable apps. Leave a short docs link.

**Subject:** A few best practices for building on FalkorDB

This is the last email in this short series. Here are a few best practices to help you build fast, reliable applications on FalkorDB.

**Best practices**

- **Index what you MATCH or MERGE on.** It turns full label scans into direct lookups and speeds up writes. Indexing guide: <https://docs.falkordb.com/cypher/indexing/>
- **Send reads to replicas.** Use GRAPH.RO_QUERY so the primary stays free for writes and reads scale out.
- **Shard writes across graphs.** Writes to one graph are serialized, so split work across graphs to write in parallel.
- **Keep writes short.** A long write holds the graph and stalls everything queued behind it.
- **Use a graph naming convention.** Prefixes enable access scoping, sharding, and per tenant isolation.
- **Lock down access with ACL roles.** Read only or read write per graph prefix protects your data.
- **Bulk load with the right tool.** The bulk loader and batched UNWIND beat row by row CREATE. Bulk loader: <https://docs.falkordb.com/integration/bulk-loader>
- **Keep memory under about 75 percent.** It leaves headroom for query memory and save forks.

**Start your free trial:** <https://app.falkordb.cloud/signin> · **Read the docs:** <https://docs.falkordb.com/getting-started/>

Thanks for spending the week with FalkorDB. No need to reply unless we can help with something specific.

Regards,

The FalkorDB Team

---

## After this flow

Contacts move into the database aware journeys (Free DB, Paid DB, Churn) based on what happens in their account.
