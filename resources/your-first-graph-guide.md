# Your First Graph on FalkorDB — A Step-by-Step Guide

> **⚠️ DRAFT** — This document is a work in progress and has not been finalized for general availability.

You just created a FalkorDB database. This guide walks you through building a real graph from scratch — creating nodes, adding properties, indexing for performance, and connecting everything with relationships.

We'll build a small **movie database**: actors, movies, and who acted in what.

You can follow along using **the CLI (redis-cli)** or the **Python client** — pick whichever fits your workflow.

---

## Before You Start

Grab your connection details from the [FalkorDB Cloud Console](https://app.falkordb.cloud) → your instance → **Connectivity** tab.

You'll need:
- **Host** — your instance endpoint (e.g., `my-db-xxxx.falkordb.io`)
- **Port** — `6379`
- **Password** — the one you set when creating the instance

---

## Step 0: Install the Tools

Pick your OS and install what you need.

### CLI (redis-cli)

<details>
<summary><strong>macOS</strong></summary>

```bash
brew install redis
```
</details>

<details>
<summary><strong>Ubuntu / Debian</strong></summary>

```bash
sudo apt-get update && sudo apt-get install -y redis-tools
```
</details>

<details>
<summary><strong>Windows</strong></summary>

Install via [WSL](https://learn.microsoft.com/en-us/windows/wsl/install), then:
```bash
sudo apt-get update && sudo apt-get install -y redis-tools
```

Or use [Memurai CLI](https://www.memurai.com/) as an alternative.
</details>

### Python Client

<details>
<summary><strong>macOS / Linux</strong></summary>

```bash
pip install falkordb
```
</details>

<details>
<summary><strong>Windows</strong></summary>

```bash
pip install falkordb
```

If you get permission errors, try:
```bash
pip install --user falkordb
```
</details>

---

## Step 1: Connect to Your Database

### CLI

```bash
redis-cli -h <your-host> -p 6379 -a <your-password> --tls
```

You should see a prompt like:
```
your-host:6379>
```

### Python

```python
from falkordb import FalkorDB

db = FalkorDB(
    host="<your-host>",
    port=6379,
    password="<your-password>",
    ssl=True
)

graph = db.select_graph("movies")
print("Connected!")
```

---

## Step 2: Create Your First Nodes

Let's add some actors and movies. In FalkorDB, a **node** is an entity with a **label** (its type) and **properties** (its data).

### CLI

```bash
GRAPH.QUERY movies "CREATE (:Actor {name: 'Keanu Reeves', born: 1964})"
GRAPH.QUERY movies "CREATE (:Actor {name: 'Carrie-Anne Moss', born: 1967})"
GRAPH.QUERY movies "CREATE (:Actor {name: 'Laurence Fishburne', born: 1961})"
```

```bash
GRAPH.QUERY movies "CREATE (:Movie {title: 'The Matrix', released: 1999, genre: 'Sci-Fi'})"
GRAPH.QUERY movies "CREATE (:Movie {title: 'John Wick', released: 2014, genre: 'Action'})"
```

### Python

```python
graph.query("CREATE (:Actor {name: 'Keanu Reeves', born: 1964})")
graph.query("CREATE (:Actor {name: 'Carrie-Anne Moss', born: 1967})")
graph.query("CREATE (:Actor {name: 'Laurence Fishburne', born: 1961})")

graph.query("CREATE (:Movie {title: 'The Matrix', released: 1999, genre: 'Sci-Fi'})")
graph.query("CREATE (:Movie {title: 'John Wick', released: 2014, genre: 'Action'})")

print("Nodes created!")
```

> **What just happened?** You created 5 nodes — 3 with the label `Actor` and 2 with the label `Movie`. Each node has properties like `name`, `born`, `title`, etc.

---

## Step 3: Add an Index

Before your graph grows, add indexes on the properties you'll search by. This makes lookups fast.

### CLI

```bash
GRAPH.QUERY movies "CREATE INDEX FOR (a:Actor) ON (a.name)"
GRAPH.QUERY movies "CREATE INDEX FOR (m:Movie) ON (m.title)"
```

### Python

```python
graph.query("CREATE INDEX FOR (a:Actor) ON (a.name)")
graph.query("CREATE INDEX FOR (m:Movie) ON (m.title)")

print("Indexes created!")
```

> **Why index now?** Indexes speed up `MATCH` queries that filter by a property. Adding them early is a good habit — it's painless now and saves you from slow queries later.

---

## Step 4: Connect Nodes with Relationships

Now the fun part — **relationships** are what make a graph a graph. Let's connect actors to the movies they appeared in.

### CLI

```bash
GRAPH.QUERY movies "MATCH (a:Actor {name: 'Keanu Reeves'}), (m:Movie {title: 'The Matrix'}) CREATE (a)-[:ACTED_IN {role: 'Neo'}]->(m)"
GRAPH.QUERY movies "MATCH (a:Actor {name: 'Keanu Reeves'}), (m:Movie {title: 'John Wick'}) CREATE (a)-[:ACTED_IN {role: 'John Wick'}]->(m)"
GRAPH.QUERY movies "MATCH (a:Actor {name: 'Carrie-Anne Moss'}), (m:Movie {title: 'The Matrix'}) CREATE (a)-[:ACTED_IN {role: 'Trinity'}]->(m)"
GRAPH.QUERY movies "MATCH (a:Actor {name: 'Laurence Fishburne'}), (m:Movie {title: 'The Matrix'}) CREATE (a)-[:ACTED_IN {role: 'Morpheus'}]->(m)"
```

### Python

```python
graph.query("""
    MATCH (a:Actor {name: 'Keanu Reeves'}), (m:Movie {title: 'The Matrix'})
    CREATE (a)-[:ACTED_IN {role: 'Neo'}]->(m)
""")

graph.query("""
    MATCH (a:Actor {name: 'Keanu Reeves'}), (m:Movie {title: 'John Wick'})
    CREATE (a)-[:ACTED_IN {role: 'John Wick'}]->(m)
""")

graph.query("""
    MATCH (a:Actor {name: 'Carrie-Anne Moss'}), (m:Movie {title: 'The Matrix'})
    CREATE (a)-[:ACTED_IN {role: 'Trinity'}]->(m)
""")

graph.query("""
    MATCH (a:Actor {name: 'Laurence Fishburne'}), (m:Movie {title: 'The Matrix'})
    CREATE (a)-[:ACTED_IN {role: 'Morpheus'}]->(m)
""")

print("Relationships created!")
```

> **What's the pattern?** `(a)-[:ACTED_IN {role: 'Neo'}]->(m)` — this is Cypher's ASCII-art syntax. The arrow `->` shows direction, `ACTED_IN` is the relationship type, and `{role: 'Neo'}` is a property on the relationship itself.

---

## Step 5: Query Your Graph

Now let's ask some questions.

### Who acted in The Matrix?

**CLI:**
```bash
GRAPH.QUERY movies "MATCH (a:Actor)-[r:ACTED_IN]->(m:Movie {title: 'The Matrix'}) RETURN a.name AS Actor, r.role AS Role"
```

**Python:**
```python
result = graph.query("""
    MATCH (a:Actor)-[r:ACTED_IN]->(m:Movie {title: 'The Matrix'})
    RETURN a.name AS Actor, r.role AS Role
""")

for row in result.result_set:
    print(f"{row[0]} played {row[1]}")
```

**Output:**
```
Keanu Reeves played Neo
Carrie-Anne Moss played Trinity
Laurence Fishburne played Morpheus
```

### What movies did Keanu Reeves act in?

**CLI:**
```bash
GRAPH.QUERY movies "MATCH (a:Actor {name: 'Keanu Reeves'})-[:ACTED_IN]->(m:Movie) RETURN m.title AS Movie, m.released AS Year"
```

**Python:**
```python
result = graph.query("""
    MATCH (a:Actor {name: 'Keanu Reeves'})-[:ACTED_IN]->(m:Movie)
    RETURN m.title AS Movie, m.released AS Year
""")

for row in result.result_set:
    print(f"{row[0]} ({row[1]})")
```

**Output:**
```
The Matrix (1999)
John Wick (2014)
```

### Who else was in a movie with Keanu?

**CLI:**
```bash
GRAPH.QUERY movies "MATCH (keanu:Actor {name: 'Keanu Reeves'})-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(coactor:Actor) RETURN coactor.name AS CoActor, m.title AS Movie"
```

**Python:**
```python
result = graph.query("""
    MATCH (keanu:Actor {name: 'Keanu Reeves'})-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(coactor:Actor)
    RETURN coactor.name AS CoActor, m.title AS Movie
""")

for row in result.result_set:
    print(f"{row[0]} — in {row[1]}")
```

**Output:**
```
Carrie-Anne Moss — in The Matrix
Laurence Fishburne — in The Matrix
```

---

## Step 6: Explore in the Browser UI

Head to your [FalkorDB Cloud Console](https://app.falkordb.cloud), open your instance, and try running queries in the built-in graph browser. You can visualize nodes and relationships as an interactive graph — it's the fastest way to explore your data.

Try pasting this in the query box:
```cypher
MATCH (a)-[r]->(m) RETURN a, r, m
```

---

## What's Next?

You've got a working graph. Here are some ideas for where to go next:

| What | Link |
|------|------|
| Learn more Cypher | [Cypher Reference](https://docs.falkordb.com/cypher/) |
| Add full-text or vector search | [Indexing Guide](https://docs.falkordb.com/cypher/indexing/) |
| Build GraphRAG with AI | [GraphRAG SDK](https://docs.falkordb.com/genai-tools/graphrag-sdk) |
| Try other languages (JS, Go, Java, Rust, C#) | [Client Libraries](https://docs.falkordb.com/getting-started/clients.html) |
| Join the community | [Discord](https://discord.gg/falkordb) |

---

**Need help?** Reply to this message, email us at **support@falkordb.com**, or join our [Discord](https://discord.gg/falkordb).
