# FalkorDB Use Case Examples

> **⚠️ DRAFT** — This document is a work in progress and has not been finalized for general availability.

Real-world examples showing how to model and query graph data with FalkorDB. Each use case includes a schema overview, sample data, and practical Cypher queries.

For more information, see [docs.falkordb.com](https://docs.falkordb.com/).

---

## 1. Social Network

**Description:** Model users, friendships, posts, and interactions. Graph databases excel at social features like friend-of-friend recommendations, feed ranking, and community detection.

### Schema

- **Nodes:** `User`, `Post`
- **Relationships:** `FOLLOWS`, `POSTED`, `LIKED`, `COMMENTED_ON`

### Sample Data

```cypher
CREATE (alice:User {name: 'Alice', joinedAt: '2023-01-15'})
CREATE (bob:User {name: 'Bob', joinedAt: '2023-02-20'})
CREATE (carol:User {name: 'Carol', joinedAt: '2023-03-10'})
CREATE (dave:User {name: 'Dave', joinedAt: '2023-04-05'})

CREATE (alice)-[:FOLLOWS]->(bob)
CREATE (alice)-[:FOLLOWS]->(carol)
CREATE (bob)-[:FOLLOWS]->(carol)
CREATE (carol)-[:FOLLOWS]->(dave)

CREATE (alice)-[:POSTED]->(p1:Post {content: 'Hello world!', createdAt: '2023-05-01'})
CREATE (bob)-[:LIKED]->(p1)
CREATE (carol)-[:LIKED]->(p1)
```

### Example Queries

**Friend-of-friend recommendations:**
```cypher
MATCH (me:User {name: 'Alice'})-[:FOLLOWS]->(friend)-[:FOLLOWS]->(suggestion)
WHERE suggestion <> me AND NOT (me)-[:FOLLOWS]->(suggestion)
RETURN suggestion.name, count(friend) AS mutualConnections
ORDER BY mutualConnections DESC
```

**User's feed (posts from people they follow):**
```cypher
MATCH (me:User {name: 'Alice'})-[:FOLLOWS]->(friend)-[:POSTED]->(post:Post)
RETURN friend.name, post.content, post.createdAt
ORDER BY post.createdAt DESC
LIMIT 20
```

**Most popular posts:**
```cypher
MATCH (post:Post)<-[:LIKED]-(user:User)
RETURN post.content, count(user) AS likes
ORDER BY likes DESC
LIMIT 10
```

---

## 2. Fraud Detection

**Description:** Detect fraud rings by identifying shared attributes across accounts — same device, phone number, address, or IP. Graphs make it easy to spot suspicious clusters that are invisible in tabular data.

### Schema

- **Nodes:** `Account`, `Transaction`, `Device`, `Phone`, `Address`, `IP`
- **Relationships:** `MADE_TRANSACTION`, `USED_DEVICE`, `HAS_PHONE`, `HAS_ADDRESS`, `FROM_IP`

### Sample Data

```cypher
CREATE (a1:Account {id: 'ACC001', name: 'John', status: 'active'})
CREATE (a2:Account {id: 'ACC002', name: 'Jane', status: 'active'})
CREATE (a3:Account {id: 'ACC003', name: 'FakeJohn', status: 'flagged'})

CREATE (d1:Device {fingerprint: 'DEV-XYZ-123'})
CREATE (p1:Phone {number: '+1-555-0100'})

CREATE (a1)-[:USED_DEVICE]->(d1)
CREATE (a3)-[:USED_DEVICE]->(d1)
CREATE (a1)-[:HAS_PHONE]->(p1)
CREATE (a3)-[:HAS_PHONE]->(p1)

CREATE (a1)-[:MADE_TRANSACTION]->(t1:Transaction {amount: 500, timestamp: '2024-01-15'})
CREATE (a3)-[:MADE_TRANSACTION]->(t2:Transaction {amount: 5000, timestamp: '2024-01-15'})
```

### Example Queries

**Find accounts sharing devices (potential fraud ring):**
```cypher
MATCH (a1:Account)-[:USED_DEVICE]->(d:Device)<-[:USED_DEVICE]-(a2:Account)
WHERE a1 <> a2
RETURN a1.id, a2.id, d.fingerprint
```

**Detect accounts with multiple shared attributes:**
```cypher
MATCH (a1:Account)-[:USED_DEVICE|HAS_PHONE|HAS_ADDRESS]->(shared)<-[:USED_DEVICE|HAS_PHONE|HAS_ADDRESS]-(a2:Account)
WHERE a1 <> a2
RETURN a1.id, a2.id, labels(shared), count(shared) AS sharedAttributes
ORDER BY sharedAttributes DESC
```

**High-value transactions from flagged accounts:**
```cypher
MATCH (a:Account {status: 'flagged'})-[:MADE_TRANSACTION]->(t:Transaction)
WHERE t.amount > 1000
RETURN a.id, a.name, t.amount, t.timestamp
ORDER BY t.amount DESC
```

---

## 3. Knowledge Graph

**Description:** Store and query interconnected facts — entities, concepts, and their relationships. Power search engines, chatbots, and discovery tools with structured knowledge.

### Schema

- **Nodes:** `Entity` (with `type` property: Person, Organization, Concept, Technology)
- **Relationships:** `IS_A`, `RELATED_TO`, `CREATED_BY`, `USED_BY`, `PART_OF`

### Sample Data

```cypher
CREATE (falkor:Entity {name: 'FalkorDB', type: 'Technology'})
CREATE (graphdb:Entity {name: 'Graph Database', type: 'Concept'})
CREATE (cypher:Entity {name: 'Cypher', type: 'Technology'})
CREATE (redis:Entity {name: 'Redis', type: 'Technology'})

CREATE (falkor)-[:IS_A]->(graphdb)
CREATE (falkor)-[:USES]->(cypher)
CREATE (falkor)-[:BUILT_ON]->(redis)
```

### Example Queries

**Explore connections from an entity:**
```cypher
MATCH (e:Entity {name: 'FalkorDB'})-[r]->(related)
RETURN e.name, type(r), related.name, related.type
```

**Find shortest path between two concepts:**
```cypher
MATCH path = shortestPath(
  (a:Entity {name: 'FalkorDB'})-[*]-(b:Entity {name: 'Redis'})
)
RETURN path
```

**Discover all technologies of a given type:**
```cypher
MATCH (e:Entity {type: 'Technology'})-[:IS_A]->(concept:Entity)
RETURN e.name, concept.name
ORDER BY concept.name
```

---

## 4. Recommendation Engine

**Description:** Generate personalized recommendations using collaborative filtering and graph patterns — find items purchased by similar users, or items frequently bought together.

### Schema

- **Nodes:** `User`, `Product`, `Category`
- **Relationships:** `PURCHASED`, `VIEWED`, `RATED`, `IN_CATEGORY`

### Sample Data

```cypher
CREATE (alice:User {name: 'Alice'})
CREATE (bob:User {name: 'Bob'})

CREATE (laptop:Product {name: 'Laptop', price: 999})
CREATE (mouse:Product {name: 'Mouse', price: 29})
CREATE (keyboard:Product {name: 'Keyboard', price: 79})
CREATE (monitor:Product {name: 'Monitor', price: 349})

CREATE (electronics:Category {name: 'Electronics'})
CREATE (laptop)-[:IN_CATEGORY]->(electronics)
CREATE (mouse)-[:IN_CATEGORY]->(electronics)

CREATE (alice)-[:PURCHASED]->(laptop)
CREATE (alice)-[:PURCHASED]->(mouse)
CREATE (bob)-[:PURCHASED]->(laptop)
CREATE (bob)-[:PURCHASED]->(keyboard)
```

### Example Queries

**"Customers who bought X also bought Y":**
```cypher
MATCH (target:Product {name: 'Laptop'})<-[:PURCHASED]-(user)-[:PURCHASED]->(other:Product)
WHERE other <> target
RETURN other.name, count(user) AS coBuyers
ORDER BY coBuyers DESC
LIMIT 5
```

**Personalized recommendations for a user:**
```cypher
MATCH (me:User {name: 'Alice'})-[:PURCHASED]->(myProduct)<-[:PURCHASED]-(similar)-[:PURCHASED]->(rec:Product)
WHERE NOT (me)-[:PURCHASED]->(rec)
RETURN rec.name, rec.price, count(similar) AS score
ORDER BY score DESC
LIMIT 10
```

**Products in the same category:**
```cypher
MATCH (p:Product {name: 'Laptop'})-[:IN_CATEGORY]->(cat)<-[:IN_CATEGORY]-(related:Product)
WHERE related <> p
RETURN related.name, related.price, cat.name AS category
```

---

## 5. IT Infrastructure / Network

**Description:** Map servers, services, and dependencies to understand blast radius, plan maintenance, and diagnose outages. Graph queries make impact analysis simple.

### Schema

- **Nodes:** `Server`, `Service`, `Database`, `LoadBalancer`
- **Relationships:** `HOSTS`, `DEPENDS_ON`, `CONNECTS_TO`, `ROUTES_TO`

### Sample Data

```cypher
CREATE (lb:LoadBalancer {name: 'LB-1', ip: '10.0.0.1'})
CREATE (web1:Server {name: 'Web-1', ip: '10.0.1.1', os: 'Ubuntu'})
CREATE (web2:Server {name: 'Web-2', ip: '10.0.1.2', os: 'Ubuntu'})
CREATE (api:Service {name: 'API Service', version: '2.1'})
CREATE (db:Database {name: 'PrimaryDB', engine: 'FalkorDB'})

CREATE (lb)-[:ROUTES_TO]->(web1)
CREATE (lb)-[:ROUTES_TO]->(web2)
CREATE (web1)-[:HOSTS]->(api)
CREATE (web2)-[:HOSTS]->(api)
CREATE (api)-[:DEPENDS_ON]->(db)
```

### Example Queries

**Impact analysis — what depends on a server:**
```cypher
MATCH (s:Server {name: 'Web-1'})<-[:ROUTES_TO|DEPENDS_ON|HOSTS*1..5]-(affected)
RETURN affected.name, labels(affected)
```

**Find all services depending on a database:**
```cypher
MATCH (svc:Service)-[:DEPENDS_ON*]->(db:Database {name: 'PrimaryDB'})
RETURN svc.name, svc.version
```

**Full dependency chain for a service:**
```cypher
MATCH path = (svc:Service {name: 'API Service'})-[:DEPENDS_ON*]->(dep)
RETURN path
```

---

## 6. Supply Chain

**Description:** Model suppliers, products, warehouses, and logistics to optimize procurement, track goods, and identify supply chain risks.

### Schema

- **Nodes:** `Supplier`, `Product`, `Warehouse`, `Customer`, `Region`
- **Relationships:** `SUPPLIES`, `STORED_IN`, `SHIPPED_TO`, `LOCATED_IN`

### Sample Data

```cypher
CREATE (s1:Supplier {name: 'Acme Parts', country: 'US'})
CREATE (s2:Supplier {name: 'Global Components', country: 'DE'})
CREATE (p1:Product {sku: 'WIDGET-A', name: 'Widget A'})
CREATE (p2:Product {sku: 'GEAR-B', name: 'Gear B'})
CREATE (w1:Warehouse {name: 'East Coast Hub', city: 'Newark'})
CREATE (w2:Warehouse {name: 'EU Hub', city: 'Frankfurt'})

CREATE (s1)-[:SUPPLIES {leadTimeDays: 5}]->(p1)
CREATE (s2)-[:SUPPLIES {leadTimeDays: 14}]->(p2)
CREATE (p1)-[:STORED_IN {quantity: 500}]->(w1)
CREATE (p2)-[:STORED_IN {quantity: 200}]->(w2)
```

### Example Queries

**Find all suppliers for a product:**
```cypher
MATCH (s:Supplier)-[rel:SUPPLIES]->(p:Product {name: 'Widget A'})
RETURN s.name, s.country, rel.leadTimeDays
ORDER BY rel.leadTimeDays
```

**Warehouse inventory overview:**
```cypher
MATCH (p:Product)-[r:STORED_IN]->(w:Warehouse)
RETURN w.name, p.name, r.quantity
ORDER BY w.name, p.name
```

**Identify single-source dependencies (supply chain risk):**
```cypher
MATCH (p:Product)<-[:SUPPLIES]-(s:Supplier)
WITH p, count(s) AS supplierCount, collect(s.name) AS suppliers
WHERE supplierCount = 1
RETURN p.name, suppliers[0] AS soleSupplier
```

---

## Getting Started

1. **Choose a use case** that matches your domain
2. **Design your schema** — see the [Data Modeling Guide](./data-modeling-guide.md)
3. **Create indexes** on properties you'll query — see [Indexing & Performance Tips](./indexing-performance-tips.md)
4. **Load your data** and iterate on your queries

---

## Further Reading

- [Cypher Query Language](https://docs.falkordb.com/cypher/)
- [Data Modeling Guide](./data-modeling-guide.md)
- [Indexing & Performance Tips](./indexing-performance-tips.md)
- [FalkorDB Documentation](https://docs.falkordb.com/)
