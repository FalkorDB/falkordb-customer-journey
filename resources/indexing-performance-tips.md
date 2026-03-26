# Indexing & Performance Tips for FalkorDB

Optimize your FalkorDB queries and data operations with proper indexing, efficient query patterns, and smart data loading strategies.

For full indexing documentation, see [docs.falkordb.com/cypher/indexing](https://docs.falkordb.com/cypher/indexing).

---

## Why Indexes Matter

Without indexes, FalkorDB must scan every node of a given label to find matches. With indexes, lookups are near-instant.

**Without an index:**
```cypher
// Scans ALL Person nodes to find Alice
MATCH (p:Person {name: 'Alice'}) RETURN p
```
→ Full label scan: O(n) — slow as your graph grows.

**With an index:**
```cypher
CREATE INDEX FOR (p:Person) ON (p.name)

// Now uses the index — direct lookup
MATCH (p:Person {name: 'Alice'}) RETURN p
```
→ Index lookup: O(log n) — fast regardless of graph size.

---

## Types of Indexes

FalkorDB supports three index types, each optimized for different query patterns:

### 1. Range Index (Property Lookups)

Best for exact matches, comparisons, and range queries on property values.

```cypher
// Create a range index
CREATE INDEX FOR (p:Person) ON (p.name)
CREATE INDEX FOR (p:Person) ON (p.age)

// Queries that benefit from range indexes
MATCH (p:Person {name: 'Alice'}) RETURN p          // Exact match
MATCH (p:Person) WHERE p.age > 25 RETURN p          // Range query
MATCH (p:Person) WHERE p.age >= 20 AND p.age <= 30 RETURN p  // Range
```

**Drop a range index:**
```cypher
DROP INDEX ON :Person(name)
```

### 2. Full-Text Index (Text Search)

Best for searching within text content — articles, descriptions, comments.

```cypher
// Create a full-text index on one or more properties
CREATE FULLTEXT INDEX FOR (a:Article) ON (a.title, a.body)

// Query using full-text search
CALL db.idx.fulltext.queryNodes('Article', 'graph database')
YIELD node
RETURN node.title, node.body
```

Full-text indexes support:
- Multi-word queries
- Partial matching
- Relevance scoring

### 3. Vector Index (Similarity Search)

Best for AI/ML workloads — finding similar items based on embedding vectors.

```cypher
// Create a vector index
CREATE VECTOR INDEX FOR (d:Document) ON (d.embedding)
OPTIONS {dimension: 384, similarityFunction: 'cosine'}

// Query nearest neighbors
CALL db.idx.vector.queryNodes('Document', 'embedding', 10, vecf32($queryVector))
YIELD node, score
RETURN node.title, score
ORDER BY score DESC
```

Supported similarity functions: `cosine`, `euclidean`, `ip` (inner product).

---

## When to Index

### Index These Properties

- **Properties used in WHERE clauses** — Filtered frequently
- **Properties used in MATCH patterns** — `{name: 'Alice'}`
- **High-cardinality properties** — Many unique values (email, ID, username)
- **Properties used in ORDER BY** — Can speed up sorting

### Don't Index These

- **Low-cardinality properties** — Boolean flags, status fields with few values (small performance gain, wastes memory)
- **Properties rarely queried** — Indexes only help if queries use them
- **Every property** — Over-indexing wastes memory and slows writes

### Check Existing Indexes

```cypher
CALL db.indexes()
```

---

## Query Optimization Tips

### 1. Use PROFILE to Analyze Queries

The `PROFILE` command shows the query execution plan with actual timing and row counts:

```
GRAPH.PROFILE my_graph "MATCH (p:Person {name: 'Alice'})-[:KNOWS]->(f) RETURN f"
```

Look for:
- **Full label scans** — Add an index on the filtered property
- **High row counts** in intermediate steps — Restructure the query to filter earlier
- **Cartesian products** — Ensure patterns are connected

### 2. Filter Early

Place your most selective filters first to reduce the number of rows processed:

```cypher
// Good: Filter on indexed property first
MATCH (p:Person {name: 'Alice'})-[:KNOWS]->(f:Person)
RETURN f.name

// Bad: Broad match first, then filter
MATCH (p:Person)-[:KNOWS]->(f:Person)
WHERE p.name = 'Alice'
RETURN f.name
```

### 3. Use LIMIT

Always use `LIMIT` when you don't need all results:

```cypher
MATCH (p:Person)-[:POSTED]->(post:Post)
RETURN p.name, post.title
ORDER BY post.createdAt DESC
LIMIT 20
```

### 4. Avoid Unbounded Variable-Length Paths

Unbounded traversals can be extremely expensive:

```cypher
// Dangerous: Traverses the entire reachable graph
MATCH (a)-[*]->(b) RETURN a, b

// Better: Set a reasonable upper bound
MATCH (a)-[*1..5]->(b) RETURN a, b
```

### 5. Use Specific Relationship Types

Specifying the relationship type allows FalkorDB to skip irrelevant edges:

```cypher
// Good: Only traverses KNOWS relationships
MATCH (a:Person)-[:KNOWS]->(b:Person) RETURN b

// Slower: Traverses all relationship types
MATCH (a:Person)-[]->(b:Person) RETURN b
```

### 6. Use WITH to Control Scope

Break complex queries into stages with `WITH` to reduce intermediate result sizes:

```cypher
MATCH (p:Person)-[:LIVES_IN]->(c:City {name: 'NYC'})
WITH p
MATCH (p)-[:WORKS_AT]->(company:Company)
RETURN p.name, company.name
```

---

## Data Loading Tips

### Batch Operations with UNWIND

Use `UNWIND` for bulk inserts instead of running individual `CREATE` statements:

```cypher
// Bulk insert nodes
UNWIND $people AS person
CREATE (p:Person {name: person.name, age: person.age})
```

In Python:
```python
people = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Carol", "age": 35},
]
graph.query(
    "UNWIND $people AS person CREATE (p:Person {name: person.name, age: person.age})",
    params={"people": people}
)
```

### Bulk Insert Relationships

```cypher
UNWIND $edges AS edge
MATCH (a:Person {name: edge.from}), (b:Person {name: edge.to})
CREATE (a)-[:KNOWS]->(b)
```

### Create Indexes Before Loading

Create indexes **before** loading data so the index is populated incrementally:

```cypher
CREATE INDEX FOR (p:Person) ON (p.name)
// Then load data...
```

### Use MERGE for Idempotent Loads

When loading data that may contain duplicates, use `MERGE` to avoid creating duplicate nodes:

```cypher
UNWIND $people AS person
MERGE (p:Person {name: person.name})
ON CREATE SET p.age = person.age
```

---

## Memory Considerations

### Monitor Graph Size

Check the number of nodes and relationships:

```cypher
// Count nodes
MATCH (n) RETURN count(n)

// Count relationships
MATCH ()-[r]->() RETURN count(r)

// Count by label
MATCH (n:Person) RETURN count(n)
```

### Use Appropriate Data Types

- Use integers instead of strings for numeric values
- Keep string properties concise
- Avoid storing large blobs as properties — store a reference/URL instead

### Index Memory Impact

Each index consumes memory. Monitor your instance's memory usage and only maintain indexes that actively improve query performance.

---

## Performance Checklist

| ✅ Do                                    | ❌ Don't                                    |
|------------------------------------------|---------------------------------------------|
| Index properties used in WHERE/MATCH     | Index every property                        |
| Use LIMIT for paginated results          | Return entire graph without limits          |
| Set upper bounds on variable-length paths| Use unbounded `[*]` traversals              |
| Specify relationship types in MATCH      | Use anonymous relationships `[]->()`        |
| Use UNWIND for bulk inserts              | Run thousands of individual CREATE queries  |
| PROFILE slow queries to find bottlenecks | Guess at performance issues                 |
| Filter early with indexed properties     | Filter late after broad matches             |
| Use MERGE for idempotent data loading    | CREATE duplicates and deduplicate later     |

---

## Further Reading

- [Indexing Reference](https://docs.falkordb.com/cypher/indexing)
- [Cypher Query Language](https://docs.falkordb.com/cypher/)
- [FalkorDB Documentation](https://docs.falkordb.com/)
