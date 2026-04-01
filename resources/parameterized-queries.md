# Parameterized Queries Best Practice for FalkorDB

Write parameterized Cypher queries to improve plan-cache reuse, avoid query-injection risks, and keep your code clean. For full Cypher documentation, see [docs.falkordb.com/cypher/](https://docs.falkordb.com/cypher/).

---

## Why Parameterize?

Hardcoding values directly into query strings means FalkorDB must parse and plan a new query every time the values change. Parameterized queries solve this by separating the **query shape** (constant) from the **data** (variable):

- **Plan-cache reuse** — one compiled plan is reused for every execution.
- **Safety** — no risk of accidental Cypher injection from user input.
- **Readability** — queries stay concise; data lives in your application code.

---

## Converting to Parameterized Queries

### 1. Start From a Non-Parameterized Pattern

Typical anti-pattern — data is embedded directly in the query text:

```cypher
UNWIND [
  {id: 1, year: 2024, name: 'A'},
  {id: 2, year: 2025, name: 'B'}
] AS event
MERGE (y:Year {year: event.year})
MERGE (e:Event {id: event.id})
SET e.name = event.name
MERGE (e)-[:IN]->(y)
```

This works, but the query text changes every time the data changes.

### 2. Move Inline Data to a Parameter

Replace the inline list with `$events` so the query becomes constant:

```cypher
UNWIND $events AS event
MERGE (y:Year {year: event.year})
MERGE (e:Event {id: event.id})
SET e.name = event.name
MERGE (e)-[:IN]->(y)
```

### 3. Send the Parameter Object From Your App

Pass the data as a parameter map when executing the query.

**JavaScript / TypeScript (Neo4j-compatible driver):**

```javascript
const query = `
  UNWIND $events AS event
  MERGE (y:Year {year: event.year})
  MERGE (e:Event {id: event.id})
  SET e.name = event.name
  MERGE (e)-[:IN]->(y)
`;

const params = {
  events: [
    { id: 1, year: 2024, name: "A" },
    { id: 2, year: 2025, name: "B" },
  ],
};

await session.run(query, params);
```

**Python (FalkorDB client):**

```python
query = """
  UNWIND $events AS event
  MERGE (y:Year {year: event.year})
  MERGE (e:Event {id: event.id})
  SET e.name = event.name
  MERGE (e)-[:IN]->(y)
"""

params = {
    "events": [
        {"id": 1, "year": 2024, "name": "A"},
        {"id": 2, "year": 2025, "name": "B"},
    ]
}

graph.query(query, params=params)
```

---

## Conversion Checklist

| ✅ Do | ❌ Don't |
|-------|----------|
| Replace inline literals with `$param` or `row.field` | Build query strings by concatenating values |
| Use `UNWIND $rows AS row` for bulk operations | Loop individual queries per row |
| Prefer flat maps (`[{id, name, ...}]`) as parameters | Pass deeply nested objects |
| Keep labels and relationship types fixed in query text | Inject dynamic label/type strings |
| Use `MERGE` only for identity keys; `SET` for mutable props | MERGE on all properties |
| Add `ORDER BY` if output order matters | Assume `UNWIND` preserves order |

---

## Common Pitfalls

### Empty List Behavior

`UNWIND []` returns zero rows — the rest of the query body won't execute. If your parameter list might be empty, guard against it in your application code before calling the query.

### Query Shape Drift

Don't inject dynamic string fragments (e.g., variable label names built at runtime). Keep one reusable, fixed query shape per operation.

### Over-Nesting Payloads

Deeply nested maps can make queries harder for the optimizer to handle. Flatten your parameter structure whenever possible.

---

## Further Reading

- [Cypher Reference](https://docs.falkordb.com/cypher/)
- [Indexing & Performance Tips](indexing-performance-tips.md)
- [FalkorDB Documentation](https://docs.falkordb.com/)
