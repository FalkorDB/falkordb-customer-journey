# Cypher Cheat Sheet for FalkorDB

A quick-reference guide for writing Cypher queries on FalkorDB. For full documentation, see [docs.falkordb.com/cypher/](https://docs.falkordb.com/cypher/).

---

## Nodes

### Create a Node

```cypher
CREATE (n:Person {name: 'Alice', age: 30})
```

### Create Multiple Nodes

```cypher
CREATE (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
```

### Match Nodes

```cypher
// All nodes
MATCH (n) RETURN n

// By label
MATCH (n:Person) RETURN n

// By property
MATCH (n:Person {name: 'Alice'}) RETURN n
```

### Delete Nodes

```cypher
// Delete a specific node (must have no relationships)
MATCH (n:Person {name: 'Alice'}) DELETE n

// Delete a node and all its relationships
MATCH (n:Person {name: 'Alice'}) DETACH DELETE n

// Delete all nodes and relationships
MATCH (n) DETACH DELETE n
```

---

## Relationships

### Create a Relationship

```cypher
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
CREATE (a)-[:KNOWS {since: 2020}]->(b)
```

### Create Nodes and Relationship Together

```cypher
CREATE (a:Person {name: 'Alice'})-[:KNOWS]->(b:Person {name: 'Bob'})
```

### Match Relationship Patterns

```cypher
// Direct relationship
MATCH (a:Person)-[:KNOWS]->(b:Person) RETURN a, b

// Any direction
MATCH (a:Person)-[:KNOWS]-(b:Person) RETURN a, b

// Any relationship type
MATCH (a:Person)-[r]->(b) RETURN a, type(r), b
```

### Variable-Length Paths

```cypher
// 1 to 3 hops
MATCH (a:Person)-[:KNOWS*1..3]->(b:Person) RETURN a, b

// Any number of hops
MATCH (a:Person)-[:KNOWS*]->(b:Person) RETURN a, b

// Exact number of hops
MATCH (a:Person)-[:KNOWS*2]->(b:Person) RETURN a, b
```

---

## Filtering

### WHERE Clause

```cypher
MATCH (n:Person) WHERE n.age > 25 RETURN n
```

### Comparison Operators

| Operator | Description            |
|----------|------------------------|
| `=`      | Equal                  |
| `<>`     | Not equal              |
| `<`      | Less than              |
| `>`      | Greater than           |
| `<=`     | Less than or equal     |
| `>=`     | Greater than or equal  |

### Logical Operators

```cypher
MATCH (n:Person)
WHERE n.age > 25 AND n.name <> 'Bob'
RETURN n

MATCH (n:Person)
WHERE n.age < 20 OR n.age > 60
RETURN n
```

### String Matching

```cypher
// Contains
MATCH (n:Person) WHERE n.name CONTAINS 'li' RETURN n

// Starts with
MATCH (n:Person) WHERE n.name STARTS WITH 'Al' RETURN n

// Ends with
MATCH (n:Person) WHERE n.name ENDS WITH 'ce' RETURN n
```

### NULL Checks

```cypher
MATCH (n:Person) WHERE n.email IS NOT NULL RETURN n
MATCH (n:Person) WHERE n.email IS NULL RETURN n
```

### IN Lists

```cypher
MATCH (n:Person) WHERE n.name IN ['Alice', 'Bob', 'Carol'] RETURN n
```

---

## Aggregation

### COUNT

```cypher
MATCH (n:Person) RETURN count(n)
```

### SUM, AVG, MIN, MAX

```cypher
MATCH (n:Person) RETURN sum(n.age), avg(n.age), min(n.age), max(n.age)
```

### COLLECT (Aggregate into a List)

```cypher
MATCH (n:Person) RETURN collect(n.name)
```

### GROUP BY (Implicit)

```cypher
MATCH (n:Person) RETURN n.city, count(n) AS population
```

### ORDER BY

```cypher
MATCH (n:Person) RETURN n.name, n.age ORDER BY n.age DESC
```

### LIMIT and SKIP

```cypher
MATCH (n:Person) RETURN n ORDER BY n.name LIMIT 10
MATCH (n:Person) RETURN n ORDER BY n.name SKIP 10 LIMIT 10
```

---

## Updates

### SET Properties

```cypher
// Set a property
MATCH (n:Person {name: 'Alice'}) SET n.age = 31

// Set multiple properties
MATCH (n:Person {name: 'Alice'}) SET n.age = 31, n.city = 'NYC'

// Add a label
MATCH (n:Person {name: 'Alice'}) SET n:Employee
```

### REMOVE Properties

```cypher
// Remove a property
MATCH (n:Person {name: 'Alice'}) REMOVE n.age

// Remove a label
MATCH (n:Person {name: 'Alice'}) REMOVE n:Employee
```

---

## MERGE (Create If Not Exists)

```cypher
// Merge a node — creates only if it doesn't exist
MERGE (n:Person {name: 'Alice'})

// With ON CREATE and ON MATCH actions
MERGE (n:Person {name: 'Alice'})
ON CREATE SET n.created = timestamp()
ON MATCH SET n.lastSeen = timestamp()

// Merge a relationship
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
MERGE (a)-[:KNOWS]->(b)
```

---

## Indexes

For detailed indexing docs, see [docs.falkordb.com/cypher/indexing](https://docs.falkordb.com/cypher/indexing/).

### Range Index (Property Lookups)

```cypher
// Create
CREATE INDEX FOR (n:Person) ON (n.name)

// Drop
DROP INDEX ON :Person(name)
```

### Full-Text Index (Text Search)

```cypher
// Create
CREATE FULLTEXT INDEX FOR (n:Article) ON (n.title, n.body)

// Query
CALL db.idx.fulltext.queryNodes('Article', 'graph database') YIELD node RETURN node
```

### Vector Index (Similarity Search)

```cypher
// Create a vector index (dimension: 128, similarity: cosine)
CREATE VECTOR INDEX FOR (n:Document) ON (n.embedding)
OPTIONS {dim: 128, similarityFunction: 'cosine'}

// Query nearest neighbors
CALL db.idx.vector.queryNodes('Document', 'embedding', 5, vecf32([0.1, 0.2, ...]))
YIELD node, score
RETURN node, score
```

### List All Indexes

```cypher
CALL db.indexes()
```

---

## Common Patterns

### Shortest Path

```cypher
MATCH p = shortestPath((a:Person {name: 'Alice'})-[*]-(b:Person {name: 'Dave'}))
RETURN p
```

### OPTIONAL MATCH

```cypher
// Returns the person even if they have no friends
MATCH (n:Person {name: 'Alice'})
OPTIONAL MATCH (n)-[:KNOWS]->(friend:Person)
RETURN n.name, friend.name
```

### UNWIND (Iterate Over a List)

```cypher
// Create multiple nodes from a list
UNWIND ['Alice', 'Bob', 'Carol'] AS name
CREATE (n:Person {name: name})
```

### WITH (Chaining Query Parts)

```cypher
MATCH (n:Person)
WITH n ORDER BY n.age DESC LIMIT 5
RETURN n.name, n.age
```

### RETURN DISTINCT

```cypher
MATCH (n:Person)-[:LIVES_IN]->(c:City)
RETURN DISTINCT c.name
```

### Type and Label Functions

```cypher
// Get relationship type
MATCH (a)-[r]->(b) RETURN type(r)

// Get node labels
MATCH (n) RETURN labels(n)

// Get node ID
MATCH (n:Person) RETURN id(n), n.name
```

---

## Further Reading

- [Cypher Reference](https://docs.falkordb.com/cypher/)
- [Indexing Guide](https://docs.falkordb.com/cypher/indexing/)
- [FalkorDB Documentation](https://docs.falkordb.com/)
