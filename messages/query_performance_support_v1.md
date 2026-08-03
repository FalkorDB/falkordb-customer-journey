# Query Performance Quick Wins
**Trigger:** Reactive support reply. Customer reports slow queries or high CPU under load.
**Send timing:** In a support reply or on request.

---

## Subject: Three quick wins for slow queries

---

Hi {First Name},

Your instance is up and running. Slow responses and high CPU usually come from a few heavy queries rather than the size of the instance. Three quick wins:

- **Index the properties you filter on**, for writes and reads: **[Indexing](https://docs.falkordb.com/cypher/indexing/)**
- **Add `LIMIT`** to retrieval queries to cut query time and the data returned: **[LIMIT](https://docs.falkordb.com/cypher/limit.html)**
- **Inspect the heavy queries** with **[GRAPH.EXPLAIN](https://docs.falkordb.com/commands/graph.explain.html)** for the plan and **[GRAPH.PROFILE](https://docs.falkordb.com/commands/graph.profile.html)** to see where the time goes

Send over your queries and use case and we can help optimize them.

Best,
The FalkorDB Team

---

*Full write-up: [Diagnose and Optimize Expensive Queries](../resources/production-best-practices.md#2-diagnose-and-optimize-expensive-queries) in the Production Best Practices guide.*
