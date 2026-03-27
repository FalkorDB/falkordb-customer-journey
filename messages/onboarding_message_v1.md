# Onboarding Message — New FalkorDB Cloud Customer (First DB Created)
**Trigger:** User creates their first database on FalkorDB Cloud
**Send timing:** Immediately upon first DB creation
**Tone:** Professional & technical

---

## Subject: Your FalkorDB database is ready — here's how to get started

---

Hi {First Name},

Your FalkorDB Cloud database is live. Here's everything you need to connect, run your first queries, and start building.

---

### 1. Connect to Your Database

Your connection details are available in the **FalkorDB Cloud Console** under the **Connectivity** tab of your instance.

| Parameter | Value |
|-----------|-------|
| **Host** | `<your-instance-endpoint>` |
| **Port** | `6379` |
| **Username** | `falkordb` |
| **Password** | Set during instance creation |
| **TLS** | Enabled by default on Cloud |

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

### 2. Create Your First Nodes and Relationships

FalkorDB uses **Cypher** — a declarative graph query language with an intuitive ASCII-art syntax for expressing patterns.

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
# Create data
g.query("CREATE (:Person {name: 'Alice', role: 'Engineer'})")
g.query("CREATE (:Person {name: 'Bob', role: 'Manager'})")
g.query("MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'}) CREATE (a)-[:REPORTS_TO]->(b)")

# Query data
result = g.query("MATCH (p:Person)-[:REPORTS_TO]->(m:Person) RETURN p.name, m.name")
for row in result.result_set:
    print(row)
```

---

### 3. Explore with the Browser UI

FalkorDB Cloud includes a built-in **graph browser** accessible directly from your console. Use it to:

- Visualize your graph schema and data
- Run and iterate on Cypher queries interactively
- Inspect node and relationship properties
- Explore query history

No additional setup required — it's available from your instance dashboard.

---

### 4. Key Concepts to Know

| Concept | Description |
|---------|-------------|
| **Node** | An entity (e.g., `:Person`, `:Product`). Nodes have labels and properties. |
| **Relationship** | A directed connection between two nodes (e.g., `[:REPORTS_TO]`). Relationships have types and can have properties. |
| **Pattern** | The core of Cypher queries — e.g., `(a)-[:KNOWS]->(b)` matches nodes connected by a specific relationship. |
| **Index** | Create indexes on node properties for fast lookups at scale. |

**Create an index:**
```cypher
CREATE INDEX FOR (p:Person) ON (p.name)
```

---

### 5. Useful Resources

- **Documentation:** [docs.falkordb.com](https://docs.falkordb.com)
- **Cypher Reference:** [docs.falkordb.com/cypher](https://docs.falkordb.com/cypher/)
- **Client Libraries** (Python, JS, Go, Java, Rust, C#): [docs.falkordb.com/getting-started/clients](https://docs.falkordb.com/getting-started/clients.html)
- **Cloud Guide:** [docs.falkordb.com/cloud](https://docs.falkordb.com/cloud/)
- **GitHub:** [github.com/FalkorDB](https://github.com/FalkorDB)
- **Community Discord:** [discord.gg/falkordb](https://discord.gg/falkordb)

---

### Need Help?

If you run into any issues or have questions about your setup, reply to this message and our team will get back to you.

You can also reach us at **support@falkordb.com**.

— The FalkorDB Team

---

*You're receiving this because you created a new database on FalkorDB Cloud.*
