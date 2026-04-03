# Data Modeling Guide for FalkorDB

> **⚠️ DRAFT** — This document is a work in progress and has not been finalized for general availability.

A practical guide to designing effective graph schemas with FalkorDB. Well-designed data models lead to faster queries, simpler application code, and easier maintenance.

---

## When to Use a Graph Database

Graph databases like FalkorDB excel when your data has:

- **Rich relationships** — Many-to-many connections between entities (social networks, org charts, dependency trees)
- **Relationship-heavy queries** — Questions like "who knows someone who knows Alice?" or "what's the shortest path between X and Y?"
- **Flexible, evolving schemas** — No rigid table structure; add new node types and relationships without migrations
- **Traversal patterns** — Multi-hop queries that would require complex JOINs in SQL
- **Connected data discovery** — Finding patterns, clusters, and paths within your data

### When a Graph DB May Not Be the Best Fit

- Simple key-value lookups with no relationships
- Time-series data with no connections
- Large-scale analytics on flat, tabular data (use columnar/OLAP databases)

---

## Nodes vs Relationships vs Properties

### What Should Be a Node?

An entity is a good candidate for a **node** when:

- It has an identity of its own (a person, a product, a city)
- You need to connect it to multiple other entities
- You want to query for it directly
- It has a rich set of attributes

```cypher
CREATE (p:Person {name: 'Alice', email: 'alice@example.com', age: 30})
CREATE (c:Company {name: 'Acme Corp', industry: 'Technology'})
```

### What Should Be a Relationship?

Use a **relationship** when:

- You want to express how two entities are connected
- The connection has semantic meaning (WORKS_AT, PURCHASED, KNOWS)
- You may want to traverse or filter by the connection
- The connection can carry its own properties (timestamps, weights)

```cypher
MATCH (p:Person {name: 'Alice'}), (c:Company {name: 'Acme Corp'})
CREATE (p)-[:WORKS_AT {since: 2021, role: 'Engineer'}]->(c)
```

### What Should Be a Property?

Use a **property** when:

- The value is a simple attribute of the entity (name, age, email)
- You don't need to connect it to other entities
- It doesn't make sense as a standalone entity

**Good as a property:**
```cypher
CREATE (p:Person {name: 'Alice', country: 'US'})
```

**Better as a node (if you want to query by country or connect countries):**
```cypher
CREATE (p:Person {name: 'Alice'})-[:LIVES_IN]->(c:Country {name: 'US'})
```

---

## Labels and Properties

### Naming Best Practices

| Element       | Convention      | Examples                          |
|---------------|-----------------|-----------------------------------|
| Labels        | PascalCase      | `Person`, `BlogPost`, `OrderItem` |
| Relationships | UPPER_SNAKE_CASE| `WORKS_AT`, `HAS_TAG`, `PLACED_ORDER` |
| Properties    | camelCase        | `firstName`, `createdAt`, `isActive` |

### Multiple Labels

A node can have multiple labels to represent different roles or categories:

```cypher
CREATE (n:Person:Employee:Manager {name: 'Alice'})
```

**When to use multiple labels:**
- When a node plays multiple roles (a Person who is also an Employee)
- When you want to query across categories (all Employees, all Managers)
- For classification and filtering

**When NOT to use multiple labels:**
- Don't use labels to encode property values (don't use `:Active` — use `{status: 'active'}` instead)
- Don't add excessive labels — keep it meaningful

---

## Relationship Direction

Every relationship in FalkorDB has a direction, but you can query in either direction or ignore direction.

### When Direction Matters

Use directed relationships when the connection is inherently asymmetric:

```cypher
// Alice follows Bob (not necessarily mutual)
CREATE (alice)-[:FOLLOWS]->(bob)

// Alice manages Bob
CREATE (alice)-[:MANAGES]->(bob)

// Alice purchased a product
CREATE (alice)-[:PURCHASED]->(product)
```

### When Direction Doesn't Matter

For symmetric relationships, pick a consistent direction but query without specifying direction:

```cypher
// Store as directed (pick a convention)
CREATE (alice)-[:FRIENDS_WITH]->(bob)

// Query ignoring direction
MATCH (a:Person)-[:FRIENDS_WITH]-(b:Person)
WHERE a.name = 'Alice'
RETURN b.name
```

---

## Common Patterns

### Social Network

```cypher
// Schema
CREATE (u1:User {name: 'Alice', joinedAt: '2023-01-15'})
CREATE (u2:User {name: 'Bob', joinedAt: '2023-02-20'})
CREATE (u1)-[:FOLLOWS {since: '2023-03-01'}]->(u2)
CREATE (u1)-[:POSTED]->(p:Post {content: 'Hello world', createdAt: '2023-04-01'})
CREATE (u2)-[:LIKED]->(p)

// Friend-of-friend recommendations
MATCH (me:User {name: 'Alice'})-[:FOLLOWS]->(friend)-[:FOLLOWS]->(suggestion)
WHERE suggestion <> me
AND NOT (me)-[:FOLLOWS]->(suggestion)
RETURN suggestion.name, count(friend) AS mutualFriends
ORDER BY mutualFriends DESC
```

### Organizational Chart

```cypher
// Schema
CREATE (ceo:Employee {name: 'Carol', title: 'CEO'})
CREATE (vp:Employee {name: 'Dave', title: 'VP Engineering'})
CREATE (eng:Employee {name: 'Eve', title: 'Engineer'})
CREATE (ceo)-[:MANAGES]->(vp)-[:MANAGES]->(eng)
CREATE (vp)-[:BELONGS_TO]->(d:Department {name: 'Engineering'})

// Find all reports (direct and indirect) under a manager
MATCH (mgr:Employee {name: 'Carol'})-[:MANAGES*]->(report)
RETURN report.name, report.title
```

### Product Catalog

```cypher
// Schema
CREATE (p:Product {name: 'Laptop', price: 999.99})
CREATE (c:Category {name: 'Electronics'})
CREATE (t:Tag {name: 'portable'})
CREATE (p)-[:IN_CATEGORY]->(c)
CREATE (p)-[:HAS_TAG]->(t)

// Find products by category with tags
MATCH (p:Product)-[:IN_CATEGORY]->(c:Category {name: 'Electronics'})
OPTIONAL MATCH (p)-[:HAS_TAG]->(t:Tag)
RETURN p.name, p.price, collect(t.name) AS tags
```

### Knowledge Graph

```cypher
// Schema
CREATE (e1:Entity {name: 'FalkorDB', type: 'Software'})
CREATE (e2:Entity {name: 'Graph Database', type: 'Concept'})
CREATE (e3:Entity {name: 'Redis', type: 'Software'})
CREATE (e1)-[:IS_A]->(e2)
CREATE (e1)-[:BUILT_ON]->(e3)

// Discover connections between entities
MATCH path = shortestPath((a:Entity {name: 'FalkorDB'})-[*]-(b:Entity {name: 'Redis'}))
RETURN path
```

---

## Anti-Patterns

### 1. Over-Connecting

**Bad:** Creating relationships for every possible connection between nodes.

```cypher
// Don't: create a relationship just to store a derived value
CREATE (a)-[:DISTANCE {km: 50}]->(b)
CREATE (a)-[:DISTANCE {km: 80}]->(c)
CREATE (b)-[:DISTANCE {km: 30}]->(c)  // redundant if calculable
```

Only create relationships that represent meaningful connections in your domain.

### 2. Using Nodes Where Properties Suffice

**Bad:**
```cypher
CREATE (p:Person)-[:HAS_AGE]->(a:Age {value: 30})
```

**Good:**
```cypher
CREATE (p:Person {age: 30})
```

Only promote a value to a node if you need to connect it to other entities or query it as a first-class concept.

### 3. Mega-Nodes (Super Nodes)

Nodes with an extremely high number of relationships can degrade query performance. For example, a single `:Country {name: 'US'}` node connected to millions of users.

**Mitigation strategies:**
- Partition mega-nodes (e.g., by region, time period)
- Use properties instead of relationships for very common connections
- Filter early in queries to avoid scanning all connections

### 4. Storing Lists as Comma-Separated Strings

**Bad:**
```cypher
CREATE (p:Person {skills: 'python,java,go'})
```

**Good — use arrays or separate nodes:**
```cypher
CREATE (p:Person {skills: ['python', 'java', 'go']})

// Or, if skills need their own identity:
CREATE (p:Person)-[:HAS_SKILL]->(s:Skill {name: 'python'})
```

---

## Indexing Strategy

Choose which properties to index based on your query patterns. See [docs.falkordb.com/cypher/indexing](https://docs.falkordb.com/cypher/indexing/) for full details.

### Index Properties You Filter On

```cypher
// If you frequently query by name:
CREATE INDEX FOR (n:Person) ON (n.name)

// If you frequently query by email:
CREATE INDEX FOR (n:User) ON (n.email)
```

### Index High-Cardinality Properties

Properties with many unique values (email, ID, username) benefit most from indexes. Properties with few unique values (boolean flags, status enums) benefit less.

### Full-Text Indexes for Search

```cypher
CREATE FULLTEXT INDEX FOR (n:Article) ON (n.title, n.body)
```

### Don't Over-Index

- Each index uses memory and slows down writes
- Only index properties that appear in WHERE clauses or MATCH lookups
- Monitor query performance with `GRAPH.PROFILE` before and after indexing

---

## Further Reading

- [Cypher Indexing Reference](https://docs.falkordb.com/cypher/indexing/)
- [Cypher Query Language](https://docs.falkordb.com/cypher/)
- [FalkorDB Documentation](https://docs.falkordb.com/)
