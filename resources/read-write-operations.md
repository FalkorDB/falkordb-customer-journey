# Read & Write Operations in FalkorDB

> **⚠️ DRAFT** — This document is a work in progress and has not been finalized for general availability.

Understand how FalkorDB separates read and write workloads, how the primary/replica architecture works, and how to use the right query command from the CLI, Python, and Node.js.

---

## Why Read vs Write Matters

Not all queries are equal. A `MATCH ... RETURN` that fetches data is fundamentally different from a `CREATE` or `MERGE` that modifies data. FalkorDB provides two distinct commands for these two workloads:

| Command | Purpose | Where It Runs |
|---------|---------|---------------|
| `GRAPH.QUERY` | Read **and** write queries | Primary only |
| `GRAPH.RO_QUERY` | Read-only queries | Primary **or** replicas |

Using the correct command unlocks three benefits:

- **Performance** — Offload read traffic to replicas, freeing the primary for writes.
- **Safety** — `GRAPH.RO_QUERY` rejects any query that attempts to modify data, preventing accidental writes.
- **Scalability** — Add replicas to horizontally scale read throughput without touching the primary.

---

## Architecture — Primary & Replicas

FalkorDB follows a **primary/replica** replication model (historically called master/slave).

```
┌─────────────────────────────────────────────────┐
│                  Your Application                │
│                                                  │
│         Writes (CREATE, MERGE,        Reads      │
│          SET, DELETE)              (MATCH/RETURN) │
│              │                         │         │
└──────────────┼─────────────────────────┼─────────┘
               │                         │
               ▼                         ▼
        ┌─────────────┐          ┌──────────────┐
        │   Primary   │ ──────▶ │   Replica    │
        │  (read +    │  async   │  (read-only) │
        │   write)    │  repl.   │              │
        └─────────────┘          └──────────────┘
```

### How It Works

1. **Primary node** — Accepts all operations. Every write (`CREATE`, `MERGE`, `SET`, `DELETE`) must go through the primary. It can also serve reads.
2. **Replica node(s)** — Receive an asynchronous copy of data from the primary. They serve **read-only** queries using `GRAPH.RO_QUERY`. Any attempt to write to a replica will be rejected.
3. **Replication** — Changes on the primary are streamed to replicas asynchronously. There is a small replication lag (typically milliseconds), meaning replicas are **eventually consistent**.

### FalkorDB Cloud

In FalkorDB Cloud, the **Pro** and **Enterprise** tiers deploy a primary with one or more replicas across availability zones automatically. The platform handles failover — if the primary goes down, a replica is promoted.

| Tier | Topology |
|------|----------|
| Free | Single instance (no replication) |
| Startup | Standalone (no replication) |
| Pro | Primary + Replica (High Availability) |
| Enterprise | Primary + Replica(s), multi-zone, VPC |

---

## The Two Query Commands

### GRAPH.QUERY — Read & Write

Use `GRAPH.QUERY` for any query that **modifies** data. It can also execute read-only queries, but those are better served by `GRAPH.RO_QUERY` when replicas are available.

Write operations include:
- `CREATE` — Create nodes and relationships
- `MERGE` — Create if not exists
- `SET` — Update properties
- `DELETE` / `DETACH DELETE` — Remove nodes and relationships

### GRAPH.RO_QUERY — Read-Only

Use `GRAPH.RO_QUERY` for queries that **only read** data. This command:
- Can be routed to **replica** nodes, reducing load on the primary
- Returns an **error** if the query attempts any write operation
- Benefits from the same query plan caching as `GRAPH.QUERY`

---

## Code Examples — CLI

### Writing Data

Use `GRAPH.QUERY` to create nodes and relationships:

```shell
# Create a social graph with people and friendships
GRAPH.QUERY social "CREATE
  (alice:Person {name: 'Alice', age: 30}),
  (bob:Person {name: 'Bob', age: 25}),
  (carol:Person {name: 'Carol', age: 35}),
  (alice)-[:KNOWS {since: 2020}]->(bob),
  (bob)-[:KNOWS {since: 2021}]->(carol)"
```

Update properties with `GRAPH.QUERY`:

```shell
# Update Alice's age
GRAPH.QUERY social "MATCH (p:Person {name: 'Alice'}) SET p.age = 31"
```

### Reading Data

Use `GRAPH.RO_QUERY` to read without risk of accidental writes:

```shell
# Find all people Alice knows
GRAPH.RO_QUERY social "MATCH (a:Person {name: 'Alice'})-[:KNOWS]->(friend) RETURN friend.name, friend.age"
```

```shell
# Count all nodes
GRAPH.RO_QUERY social "MATCH (n) RETURN count(n)"
```

### Error Case — Write via RO_QUERY

If you accidentally send a write query through `GRAPH.RO_QUERY`, FalkorDB rejects it:

```shell
# This will return an error
GRAPH.RO_QUERY social "CREATE (x:Person {name: 'Dave'})"
# (error) graph.RO_QUERY is a read-only command
```

---

## Code Examples — Python

### Setup

```bash
pip install FalkorDB
```

### Writing Data — `graph.query()`

```python
from falkordb import FalkorDB

# Connect to FalkorDB
db = FalkorDB(host='localhost', port=6379)
graph = db.select_graph('social')

# Create nodes and relationships
graph.query("""
    CREATE (alice:Person {name: 'Alice', age: 30}),
           (bob:Person {name: 'Bob', age: 25}),
           (carol:Person {name: 'Carol', age: 35}),
           (alice)-[:KNOWS {since: 2020}]->(bob),
           (bob)-[:KNOWS {since: 2021}]->(carol)
""")

# Update with parameters
graph.query(
    "MATCH (p:Person {name: $name}) SET p.age = $new_age",
    params={"name": "Alice", "new_age": 31}
)
```

### Reading Data — `graph.ro_query()`

```python
# Read-only query — safe to run on replicas
result = graph.ro_query(
    "MATCH (a:Person {name: $name})-[:KNOWS]->(friend) RETURN friend.name, friend.age",
    params={"name": "Alice"}
)

for row in result.result_set:
    print(f"{row[0]}, age {row[1]}")
# Output: Bob, age 25
```

### Bulk Write with UNWIND + Read Back

```python
# Bulk insert using parameterized UNWIND
people = [
    {"name": "Dave", "age": 28},
    {"name": "Eve", "age": 33},
]

graph.query(
    "UNWIND $people AS p CREATE (:Person {name: p.name, age: p.age})",
    params={"people": people}
)

# Read back all people (read-only)
result = graph.ro_query("MATCH (p:Person) RETURN p.name, p.age ORDER BY p.name")
for row in result.result_set:
    print(row)
```

---

## Code Examples — Node.js

### Setup

```bash
npm install falkordb
```

### Writing Data — `graph.query()`

```javascript
import { FalkorDB } from 'falkordb';

const db = await FalkorDB.connect({
    socket: { host: 'localhost', port: 6379 }
});

const graph = db.selectGraph('social');

// Create nodes and relationships
await graph.query(`
    CREATE (alice:Person {name: 'Alice', age: 30}),
           (bob:Person {name: 'Bob', age: 25}),
           (carol:Person {name: 'Carol', age: 35}),
           (alice)-[:KNOWS {since: 2020}]->(bob),
           (bob)-[:KNOWS {since: 2021}]->(carol)
`);

// Update with parameters
await graph.query(
    "MATCH (p:Person {name: $name}) SET p.age = $new_age",
    { params: { name: "Alice", new_age: 31 } }
);
```

### Reading Data — `graph.roQuery()`

```javascript
// Read-only query — safe to run on replicas
const result = await graph.roQuery(
    "MATCH (a:Person {name: $name})-[:KNOWS]->(friend) RETURN friend.name, friend.age",
    { params: { name: "Alice" } }
);

for (const row of result.data) {
    console.log(`${row[0]}, age ${row[1]}`);
}
// Output: Bob, age 25
```

### Bulk Write with UNWIND + Read Back

```javascript
// Bulk insert using parameterized UNWIND
const people = [
    { name: "Dave", age: 28 },
    { name: "Eve", age: 33 },
];

await graph.query(
    "UNWIND $people AS p CREATE (:Person {name: p.name, age: p.age})",
    { params: { people } }
);

// Read back all people (read-only)
const all = await graph.roQuery(
    "MATCH (p:Person) RETURN p.name, p.age ORDER BY p.name"
);
console.log(all.data);

db.close();
```

---

## Best Practices

| ✅ Do | ❌ Don't |
|-------|----------|
| Use `GRAPH.RO_QUERY` / `ro_query()` / `roQuery()` for all read-only queries | Send every query through `GRAPH.QUERY` |
| Direct read traffic to replicas in HA deployments | Send all traffic to the primary |
| Use parameterized queries for both reads and writes | Build query strings by concatenating values |
| Use `UNWIND $rows` for bulk writes through the primary | Loop individual `CREATE` statements |
| Test write queries on a dev instance first | Run untested writes directly in production |
| Handle the RO_QUERY error gracefully in code | Assume all queries will succeed on replicas |

---

## Quick Reference

| Operation | CLI | Python | Node.js |
|-----------|-----|--------|---------|
| **Write** | `GRAPH.QUERY graph "..."` | `graph.query("...")` | `await graph.query("...")` |
| **Read** | `GRAPH.RO_QUERY graph "..."` | `graph.ro_query("...")` | `await graph.roQuery("...")` |
| **Write (params)** | `GRAPH.QUERY graph "CYPHER key='val' ..."` | `graph.query("...", params={...})` | `await graph.query("...", { params: {...} })` |
| **Read (params)** | `GRAPH.RO_QUERY graph "CYPHER key='val' ..."` | `graph.ro_query("...", params={...})` | `await graph.roQuery("...", { params: {...} })` |

---

## Further Reading

- [GRAPH.QUERY Reference](https://docs.falkordb.com/commands/graph.query.html)
- [GRAPH.RO_QUERY Reference](https://docs.falkordb.com/commands/graph.ro-query.html)
- [FalkorDB Cloud — High Availability](https://docs.falkordb.com/cloud/pro-tier.html)
- [Parameterized Queries Best Practice](parameterized-queries.md)
- [Indexing & Performance Tips](indexing-performance-tips.md)
- [FalkorDB Documentation](https://docs.falkordb.com/)
