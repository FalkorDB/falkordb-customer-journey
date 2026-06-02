# New Registrants — New Flow, Path A — Education

> **Status:** 🟢 **New — proposed, for review.** Replacement for the [legacy flow](legacy-flow.md). See the [folder README](README.md) for the overall A/B test design and shared placeholders.

**Audience:** 50% of **new registrants** in HubSpot (Path A arm of the path-level A/B test).

**Framing:** CS-led, documentation-first, no sales push. Each step links to getting-started content and self-serve resources. Cloud pricing appears as an informational link from Day 1; the Enterprise deployment link is kept out of the Day 1 welcome and only surfaces in the later steps.

**Cadence:** Day 1 → Day 3 (if no reply) → Day 6 (if no reply).

**Within-step A/B:** every step has a **Version A** and **Version B** so HubSpot can also test subject line / copy style with the path held fixed.

---

## Path A — Step 1 — Day 1

**Goal:** welcome the contact, give them the fastest path to self-serve setup, and gently encourage them to spin up a free database if they'd like to.

### Version A — "Getting started" (link-list framing)

**Subject:** Getting started with FalkorDB

Hi {First Name},

Welcome to FalkorDB! We're really glad to have you on board. We're here to help you build with graph data simply and efficiently — and because FalkorDB is built for ultra-low latency and a small memory footprint, it can meaningfully reduce the cost and size of your AI workloads. Here are the fastest links to get started:

1. **Open the FalkorDB Cloud console:** <https://app.falkordb.cloud/signin>
2. **Cloud getting started guide:** <https://docs.falkordb.com/cloud>
3. **Build your first graph (10 min walkthrough):** <https://docs.falkordb.com/getting-started/>
4. **Browser UI — visualize and query your graph:** <https://docs.falkordb.com/browser/>
5. **Cypher cheat sheet:** <https://docs.falkordb.com/cypher/>

Whenever you're ready, the best way to get a feel for FalkorDB is to spin up a **free database** — it takes a couple of minutes and there's no cost to try. No pressure at all; it's there whenever you'd like to explore.

**Create your free database →** <https://app.falkordb.cloud/signin>

Curious about the Cloud tiers? You can read through them here: **Cloud plans and pricing:** {Cloud pricing link}.

Regards,

The FalkorDB Team

### Version B — "10 minutes to first query" (single-CTA framing)

**Subject:** 10 minutes from sign-up to your first graph query

Hi {First Name},

Welcome to FalkorDB — we're excited to have you with us! The fastest way to see what FalkorDB can do is to spin up a **free database** and run a query against your own graph. It's free to try, takes a couple of minutes, and most teams get to their first query in under 10. And because FalkorDB is built for ultra-low latency and a small memory footprint, it can meaningfully reduce the cost and size of your AI workloads.

**Create your free database →** <https://app.falkordb.cloud/signin>

Then follow the quick walkthrough to build your first graph: <https://docs.falkordb.com/getting-started/>

Once your database is up, the **[Browser UI](https://docs.falkordb.com/browser/)** lets you visualize and query the graph without writing any client code.

Of course, there's no rush — it's there whenever you'd like to explore.

Want to learn about the Cloud tiers? Here's an overview: **Cloud plans and pricing:** {Cloud pricing link}

Regards,

The FalkorDB Team

---

## Path A — Step 2 — Day 3 (if no reply)

**Goal:** help contacts who have not replied move from "signed up" to "first query," without pressure.

### Version A — "Setup checklist" (numbered checklist framing)

**Subject:** A short FalkorDB setup checklist

Hi {First Name},

Hope you're enjoying exploring FalkorDB so far! If you're still getting set up, here's a short checklist that takes most teams under 15 minutes end-to-end:

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

### Version B — "Pick your client library" (developer-stack framing)

**Subject:** Connect FalkorDB from your stack

Hi {First Name},

Glad to have you building with FalkorDB! Whatever stack you're on, there's a first-class FalkorDB client — pick yours and you'll have a connection open in a few minutes:

- **Python:** <https://docs.falkordb.com/getting-started/clients.html>
- **Node.js / TypeScript:** <https://docs.falkordb.com/getting-started/clients.html>
- **Java, Go, Rust, C#, PHP:** <https://docs.falkordb.com/getting-started/clients.html>

Once connected:

- Run your first Cypher query — **[Cypher reference](https://docs.falkordb.com/cypher/)**.
- Visualize and explore your graph in the **[Browser UI](https://docs.falkordb.com/browser/)** — no client code required.

**Cloud plans and pricing:** {Cloud pricing link} · **Enterprise deployment:** {Enterprise deployment link}

Regards,

The FalkorDB Team

---

## Path A — Step 3 — Day 6 (if no reply)

**Goal:** close the generic education flow politely and leave one consolidated resource list. After this email, contacts continue in the appropriate DB-aware journey (Free or Paid).

### Version A — "All resources in one place" (comprehensive index)

**Subject:** FalkorDB resources in one place

Hi {First Name},

Thanks for spending the last week with FalkorDB! This is the last email in this short getting-started series — all the FalkorDB resources you may need are below:

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

### Version B — "Bookmark these three" (minimalist framing)

**Subject:** Three FalkorDB links worth bookmarking

Hi {First Name},

Thanks for being part of the FalkorDB community! Last email in this short series — if you only bookmark three things, make it these:

1. **Docs home** — everything you'll need as you go: <https://docs.falkordb.com/>
2. **Browser UI** — visualize and query your graph without writing client code: <https://docs.falkordb.com/browser/>
3. **Cloud console** — manage databases and billing: <https://app.falkordb.cloud/signin>

If it's useful to learn more about the Cloud tiers or self-hosted options:

- **Cloud plans and pricing:** {Cloud pricing link}
- **Enterprise deployment:** {Enterprise deployment link}

And if you ever get stuck, our community is active on **[Discord](https://discord.gg/AEHAVvH5GU)** and **[GitHub Discussions](https://github.com/orgs/FalkorDB/discussions)**.

Regards,

The FalkorDB Team
