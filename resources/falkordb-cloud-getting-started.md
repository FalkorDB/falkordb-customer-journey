# Getting Started with FalkorDB Cloud

Welcome to FalkorDB Cloud. This guide will take you from a freshly created database to running your first graph queries in minutes.

---

## 1. Connect to Your Database

Your connection details are in the **FalkorDB Cloud Console** under the **Connectivity** tab of your instance.

| Parameter | Value |
|-----------|-------|
| **Host** | `<your-instance-endpoint>` |
| **Port** | `6379` |
| **Username** | `falkordb` |
| **Password** | Set during instance creation |
| **TLS** | Enabled by default |

Install the Python client:

```bash
pip install falkordb
```

Connect and select your graph:

```python
from falkordb import FalkorDB

client = FalkorDB(
    host="<your-instance-endpoint>",
    port=6379,
    password="<your-password>",
    ssl=True
)

g = client.select_graph("my_graph")
```

---

## 2. Create Your First Nodes and Relationships

FalkorDB uses **Cypher** — a declarative graph query language with an intuitive ASCII-art syntax for expressing graph patterns.

**Create nodes:**
```cypher
CREATE (:Person {name: 'Alice', role: 'Engineer'})
CREATE (:Person {name: 'Bob', role: 'Manager'})
```

**Create a relationship:**
```cypher
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
CREATE (a)-[:REPORTS_TO]->(b)
```

**Query your graph:**
```cypher
MATCH (p:Person)-[:REPORTS_TO]->(m:Person)
RETURN p.name AS Employee, m.name AS Manager
```

Run these from Python:

```python
g.query("CREATE (:Person {name: 'Alice', role: 'Engineer'})")
g.query("CREATE (:Person {name: 'Bob', role: 'Manager'})")
g.query("MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'}) CREATE (a)-[:REPORTS_TO]->(b)")

result = g.query("MATCH (p:Person)-[:REPORTS_TO]->(m:Person) RETURN p.name, m.name")
for row in result.result_set:
    print(row)
```

---

## 3. Explore with the Browser UI

FalkorDB Cloud includes a built-in **graph browser** accessible directly from your instance dashboard — no setup required. Use it to:

- Visualize your graph schema and data
- Run and iterate on Cypher queries interactively
- Inspect node and relationship properties
- Review query history

---

## 4. Key Concepts

| Concept | Description |
|---------|-------------|
| **Node** | An entity with a label (e.g., `:Person`) and properties. |
| **Relationship** | A directed connection between two nodes (e.g., `[:REPORTS_TO]`). Relationships have types and can carry properties. |
| **Pattern** | The core of Cypher — e.g., `(a)-[:KNOWS]->(b)` matches nodes connected by a specific relationship type. |
| **Index** | Speeds up property lookups at scale. |

**Create an index:**
```cypher
CREATE INDEX FOR (p:Person) ON (p.name)
```

---

## 5. Resources

| Resource | Link |
|----------|------|
| Documentation | [docs.falkordb.com](https://docs.falkordb.com) |
| Cypher Reference | [docs.falkordb.com/cypher](https://docs.falkordb.com/cypher/) |
| Client Libraries | [docs.falkordb.com/getting-started/clients](https://docs.falkordb.com/getting-started/clients.html) |
| Cloud Guide | [docs.falkordb.com/cloud](https://docs.falkordb.com/cloud/) |
| GitHub | [github.com/FalkorDB](https://github.com/FalkorDB) |
| Community Discord | [discord.gg/falkordb](https://discord.gg/falkordb) |

---

## Need Help?

Open a support ticket at **support@falkordb.com** or reach us on [Discord](https://discord.gg/falkordb).
