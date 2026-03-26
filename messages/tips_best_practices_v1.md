# Tips & Best Practices
**Trigger:** Proactive — sent to all new users
**Send timing:** Day 3–5 after signup

---

## Subject: 3 tips to get the most out of FalkorDB

---

Hi {First Name},

Here are three practical tips to help you get the most out of FalkorDB:

---

### 1. Use indexes for faster lookups

As your graph grows, indexes make a huge difference. Create them on properties you query frequently:

```cypher
CREATE INDEX FOR (p:Person) ON (p.name)
```

📖 Learn more: **[Indexing Guide](https://docs.falkordb.com/cypher/indexing)**

---

### 2. Use the browser UI to visualize and iterate

FalkorDB Cloud includes a built-in graph browser — use it to visualize your data, run queries interactively, and inspect node and relationship properties. It's a great way to explore your graph and refine queries before putting them into code.

---

### 3. Use MERGE instead of CREATE to avoid duplicates

When loading data, `MERGE` ensures you don't create duplicate nodes or relationships. It creates the pattern only if it doesn't already exist:

```cypher
MERGE (p:Person {name: 'Alice'})
SET p.role = 'Engineer'
```

📖 Learn more: **[MERGE Reference](https://docs.falkordb.com/cypher/merge)**

---

Have questions? Reply to this message — we're happy to help.

— The FalkorDB Team

---

*You're receiving this because you recently signed up for FalkorDB Cloud.*
