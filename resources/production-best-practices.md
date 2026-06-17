# Production Best Practices for FalkorDB

> **⚠️ DRAFT** — This document is a work in progress and has not been finalized for general availability.

A practical checklist for running FalkorDB reliably and at scale: indexing, read/write separation, sharding writes across graphs, access control, bulk loading, and memory headroom.

These practices build on the focused guides linked throughout — start here, then drill into the detailed resource for any topic.

---

## TL;DR Checklist

| # | Practice | Why it matters |
|---|----------|----------------|
| 1 | **Index every property you `MATCH` or `MERGE` on** | Turns full label scans into direct lookups; also speeds up writes and `MERGE` |
| 2 | **Send reads to replicas with `GRAPH.RO_QUERY`** | Frees the primary for writes and scales read throughput |
| 3 | **Shard writes across multiple graphs** | Writes to one graph are serialized; multiple graphs write in parallel |
| 4 | **Keep write queries short and non-blocking** | A long write holds the graph and stalls everything queued behind it |
| 5 | **Adopt a graph naming convention (prefixes)** | Enables ACL scoping, sharding, and per-tenant isolation |
| 6 | **Lock down access with ACL roles** | Read-only vs read-write per graph prefix protects your data |
| 7 | **Bulk-load with the right tool** | The bulk loader and batched `UNWIND` are far faster than row-by-row `CREATE` |
| 8 | **Keep memory under ~75% of the container** | Leaves headroom for query working memory and fork-on-save (CoW) |

---

## 1. Index Everything You Match On (Most Important)

Indexes are the single highest-impact change you can make. Without one, every
`MATCH (p:Person {email: ...})` scans **all** `:Person` nodes — O(n) and slower as
the graph grows. With one, it's a direct O(log n) lookup.

```cypher
-- Create before you load or query at scale
CREATE INDEX FOR (p:Person) ON (p.email)
CREATE INDEX FOR (o:Order)  ON (o.id)
```

Indexes help **writes too**, not just reads:

- **`MERGE` depends on them.** `MERGE (p:Person {email: $e})` does a lookup first;
  without an index that lookup is a full scan on every upsert, which is the most
  common cause of slow loads.
- Faster relationship creation when you `MATCH` both endpoints by an indexed key.

**Trade-off:** indexes consume extra memory and add a small per-write maintenance
cost. Index the properties you actually filter, join, or merge on — not every
property. Audit with:

```cypher
CALL db.indexes()
```

Range, full-text, and vector indexes each suit different queries — see
**[Indexing & Performance Tips](indexing-performance-tips.md)** and the
[Indexing docs](https://docs.falkordb.com/cypher/indexing/).

---

## 2. Separate Reads from Writes

FalkorDB uses a **primary/replica** model. Use the command that matches the workload:

| Command | Workload | Runs on |
|---------|----------|---------|
| `GRAPH.QUERY` | Reads **and** writes | Primary only |
| `GRAPH.RO_QUERY` | Read-only | Primary **or** replicas |

- Route read traffic to **replicas** with `GRAPH.RO_QUERY` to keep the primary
  free for writes and to scale reads horizontally.
- `GRAPH.RO_QUERY` also **rejects accidental writes**, so it's a safety net.
- Replicas are **eventually consistent** (async replication, ~ms lag). If a read
  must see a just-written value, either read from the primary or use `WAIT` —
  see **[Wait for Replication](wait-for-replication.md)**.

Details and client examples: **[Read & Write Operations](read-write-operations.md)**.

---

## 3. Scale Writes by Sharding Across Multiple Graphs

Writes to a **single graph are serialized** — one writer holds the graph while it
runs. Reads, by contrast, run concurrently across the thread pool (`THREAD_COUNT`,
which defaults to the number of logical cores) and across replicas.

The implication: **a single graph's write throughput is bounded by one core.**
To scale writes, split data across multiple graph keys that can be written in
parallel:

```
tenant:001   tenant:002   tenant:003   ...     ← written concurrently
   │             │             │
   └── writer ───┴── writer ───┴── writer       up to THREAD_COUNT in parallel
```

Good sharding keys: **per tenant, per region, per time window, or a hash bucket**
(`shard:00` … `shard:NN`). This also keeps individual graphs smaller, which makes
saves, replication, and per-graph memory reporting cheaper.

> Avoid the opposite anti-pattern: funnelling every tenant's writes into one giant
> shared graph, which serializes all of them through a single writer.

---

## 4. Keep Write Queries Short and Non-Blocking

Because a write holds the graph, one slow write delays everything queued behind it
(and queries beyond `MAX_QUEUED_QUERIES` are rejected). Keep writes small and fast:

- **Optimize the write itself** — index the keys it looks up (see #1), `MATCH` by
  indexed properties, and avoid unbounded `MATCH` patterns inside a write.
- **Bound the batch size.** Prefer many medium `UNWIND` batches (1k–10k rows) over
  one massive transaction that holds the graph for seconds.
- **Throttle write concurrency on the client.** Too many writer threads hammering
  the same graph just queue up — reduce the concurrent write load or spread it
  across shards (see #3).
- **Use [parameterized queries](parameterized-queries.md)** so plans are cached and
  query text stays small.
- **Set guardrails:** `TIMEOUT` / `TIMEOUT_MAX` to cap runaway queries and
  `QUERY_MEM_CAPACITY` to kill any single query that allocates too much memory.

```sh
redis-cli GRAPH.CONFIG SET TIMEOUT_MAX 10000          # ms, hard cap per query
redis-cli GRAPH.CONFIG SET QUERY_MEM_CAPACITY 1073741824   # 1 GiB per query
```

---

## 5. Graph Naming Conventions

A graph name is a Redis key, so a consistent scheme pays off for access control,
sharding, and operations.

**Recommended:** a `prefix:scope` structure using `:` as the separator.

```
acme:orders          # <tenant>:<entity>
prod:users           # <env>:<entity>
shard:042            # <shard-bucket>
analytics:2026-06    # <domain>:<time-window>
```

Guidelines:

- Pick **one separator** (`:` is conventional for Redis keys and works cleanly with
  ACL glob patterns like `~acme:*`).
- Put the **most significant grouping first** (tenant/env), so a single prefix
  selects a whole class of graphs.
- Use lowercase, no spaces or special characters; keep names stable (renaming a
  graph means copy + delete).
- Encode the **environment** (`prod:` / `staging:`) when graphs share an instance.

Good naming is what makes the ACL rules in the next section concise.

---

## 6. Control Access with ACL Roles

Use Redis/FalkorDB **ACLs** to grant least-privilege access per graph prefix, so
analysts get read-only access and only services that should write can write.
Combined with a naming convention (#5), one pattern covers a whole tenant or
environment.

**Read-only analyst, scoped to one tenant:**

```text
ACL SETUSER analyst on >secret \
  +GRAPH.RO_QUERY +GRAPH.LIST \
  %R~acme:*
```

**Read-write service for the same tenant:**

```text
ACL SETUSER acme-svc on >secret \
  +GRAPH.QUERY +GRAPH.RO_QUERY +GRAPH.DELETE \
  %RW~acme:*
```

Key points:

- `%R~<pattern>` grants **read** on matching graphs; `%RW~<pattern>` grants
  **read+write**. Plain `~<pattern>` is equivalent to `%RW`.
- Patterns are globs over graph names — `~acme:*` is exactly why prefixes matter.
- You can mix scopes in one user: `%RW~acme:* %R~shared:*` (write your own
  tenant, read the shared graphs).
- `ACL SETUSER` is **in-memory only** — configure an ACL file and run `ACL SAVE`
  so users survive a restart.

See the [ACL command reference](https://docs.falkordb.com/commands/acl/).

---

## 7. Bulk & Batch Loading

Match the tool to the job:

**Large / initial loads from CSV — use the bulk loader.** It streams binary batches
through `GRAPH.BULK`, far faster than per-row `CREATE`:

```sh
pip install falkordb-bulk-loader

falkordb-bulk-insert acme:orders \
  -n Person.csv \
  -r KNOWS.csv
```

**Incremental loads from your app — batch with `UNWIND` + parameters:**

```cypher
UNWIND $rows AS row
MERGE (p:Person {id: row.id})
SET p.name = row.name
```

Send 1k–10k rows per call rather than one query per row.

Loading best practices:

- **Index your `MERGE` keys *before* loading** (#1) so each upsert is a lookup, not
  a scan.
- For pure-insert loads with no de-duplication, you can build indexes **after** the
  load (or use `DELAY_INDEXING`) to avoid per-row index maintenance.
- **During a massive load, pause RDB autosave** (`CONFIG SET save ""`) to avoid
  fork churn, then restore it afterward — while watching memory (see #8).
- Use **`WAIT`** after a critical load before reading from replicas
  ([Wait for Replication](wait-for-replication.md)).

Reference: [Bulk Loader docs](https://docs.falkordb.com/integration/bulk-loader/).

---

## 8. Memory Management — Stay Under ~75%

Keep `used_memory` below **~75%** of the container/instance limit. The remaining
headroom is not waste — it absorbs:

- **Query working memory** — joins, aggregations, and large result sets allocate
  transient memory.
- **Fork-on-save / replication** — RDB `BGSAVE` and replica sync `fork()` and rely
  on copy-on-write; under write load this can transiently inflate RSS well above
  `used_memory`. Crossing the container limit triggers an **OOM kill** (exit 137).

### Two limits to respect

1. **`maxmemory` makes the instance read only.** When `used_memory` reaches the
   configured `maxmemory`, FalkorDB rejects writes and the instance becomes read
   only until memory is freed. Set `maxmemory` to about **80 percent** of the
   memory available inside the container.
2. **The container limit triggers an OOM kill.** Fork on save and replication can
   push RSS above `used_memory`, so also leave room below the hard container limit.

### Worked example: 32 GB host

- A 32 GB host leaves about **30 GB** available inside the container after overhead.
- Set `maxmemory` to about 80 percent of that, so about **24 GB**. That is the hard
  ceiling. At 24 GB the instance turns read only.
- Keep the working dataset well below the ceiling. Aim for about **19 GB** so the
  dataset can grow and shrink without reaching 24 GB.
- The larger the instance, the larger the absolute buffer you can hold below the
  ceiling. Bigger instances are the safest option for a dataset that fluctuates.

How to stay safe:

- **Cap and monitor.** Set a Redis `maxmemory` and alert at 75%. Track
  `used_memory` and `used_memory_rss` (`INFO memory`).
- **Bound per-query memory** with `QUERY_MEM_CAPACITY` so one query can't exhaust
  the instance.
- **Right-size graphs** by sharding (#3) so no single graph dominates RAM, and a
  save fork copies less.
- **Find heavy graphs** with `GRAPH.MEMORY USAGE <graph>` (note: it reports whole
  MB and undercounts true RSS — use it for relative ranking).

```sh
redis-cli GRAPH.CONFIG SET QUERY_MEM_CAPACITY 1073741824   # 1 GiB / query
redis-cli INFO memory | grep -E 'used_memory:|used_memory_rss:|maxmemory:'
```

> **Tip:** In production, run the lighter `falkordb/falkordb-server` image (no
> bundled browser) to free memory and CPU for the database.

---

## Further Reading

| Topic | Resource |
|-------|----------|
| Indexes, query optimization, bulk loading | [Indexing & Performance Tips](indexing-performance-tips.md) |
| Primary/replica, `GRAPH.QUERY` vs `GRAPH.RO_QUERY` | [Read & Write Operations](read-write-operations.md) |
| Durable reads after writes | [Wait for Replication](wait-for-replication.md) |
| Safe, cacheable queries | [Parameterized Queries](parameterized-queries.md) |
| Schema design | [Data Modeling Guide](data-modeling-guide.md) |
| Configuration parameters | [Configuration docs](https://docs.falkordb.com/getting-started/configuration/) |
| Access control | [ACL docs](https://docs.falkordb.com/commands/acl/) |

---

Have questions? Reply to this message — we're happy to help.

— The FalkorDB Team
