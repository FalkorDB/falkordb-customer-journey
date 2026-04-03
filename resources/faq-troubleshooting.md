# FAQ & Troubleshooting — FalkorDB Cloud

> **⚠️ DRAFT** — This document is a work in progress and has not been finalized for general availability.

Common questions, issues, and solutions for FalkorDB Cloud users. For full documentation, see [docs.falkordb.com](https://docs.falkordb.com/). Join our community on [Discord](https://discord.gg/falkordb).

---

## Connection Issues

### Can't connect to my FalkorDB instance

**Checklist:**

1. **Verify host and port** — Double-check the hostname and port from your Cloud dashboard
2. **Enable TLS/SSL** — FalkorDB Cloud requires TLS. Ensure your client has `ssl=True` (Python), `tls: true` (Node.js), or the equivalent option enabled
3. **Check credentials** — Verify your username and password are correct
4. **Firewall rules** — Ensure your network/VPN allows outbound connections to the FalkorDB Cloud host and port
5. **Test connectivity** — Use `redis-cli` or `telnet` to test raw connectivity:
   ```bash
   redis-cli -h your-host -p your-port --tls -a your-password PING
   ```
6. **DNS resolution** — Ensure the hostname resolves correctly: `nslookup your-host`

### Connection timeouts

- Check your network for high latency or packet loss
- Increase the connection timeout in your client configuration
- If behind a corporate proxy, ensure it allows the connection

---

## Authentication Errors

### "WRONGPASS" or "NOAUTH" errors

- Verify your password — copy it directly from the Cloud dashboard to avoid typos
- Ensure you're passing the password in the correct client parameter
- If using a connection string, ensure special characters in the password are URL-encoded

### How to reset my password

1. Log in to the [FalkorDB Cloud dashboard](https://app.falkordb.cloud)
2. Navigate to your instance settings
3. Look for the credentials or password reset option
4. Update the password and use the new credentials in your application

---

## Query Performance

### My queries are slow

**Step 1: Check for indexes**

```cypher
CALL db.indexes()
```

If properties used in `WHERE` clauses or `MATCH` patterns are not indexed, create indexes:

```cypher
CREATE INDEX FOR (n:Person) ON (n.name)
```

**Step 2: Profile the query**

Use `GRAPH.PROFILE` to see the execution plan:

```
GRAPH.PROFILE my_graph "MATCH (p:Person {name: 'Alice'})-[:KNOWS]->(f) RETURN f"
```

Look for label scans (indicates a missing index) or high row counts in intermediate steps.

**Step 3: Optimize the query**

- Add `LIMIT` to avoid returning too many results
- Set upper bounds on variable-length paths (`[*1..5]` instead of `[*]`)
- Filter early — place the most selective conditions first
- Use specific relationship types instead of `[]->()`

See the [Indexing & Performance Tips](./indexing-performance-tips.md) guide for detailed optimization strategies.

---

## Data Import

### How to load CSV data

FalkorDB does not have a built-in `LOAD CSV` command. Instead, parse your CSV client-side and use parameterized `UNWIND` queries for batch inserts:

```python
import csv
from falkordb import FalkorDB

db = FalkorDB(host="your-host", port=6379, password="your-password", ssl=True)
graph = db.select_graph("my_graph")

with open("data.csv") as f:
    batch = [row for row in csv.DictReader(f)]

graph.query(
    "UNWIND $batch AS row CREATE (p:Person {name: row.name, age: toInteger(row.age)})",
    params={"batch": batch}
)
```

### Bulk import best practices

1. **Create indexes first** — Index properties before loading data
2. **Use UNWIND for batch inserts** — More efficient than individual CREATE statements:
   ```cypher
   UNWIND $batch AS row
   CREATE (p:Person {name: row.name, age: row.age})
   ```
3. **Use MERGE to avoid duplicates** — Especially for idempotent or repeated imports:
   ```cypher
   UNWIND $batch AS row
   MERGE (p:Person {name: row.name})
   ON CREATE SET p.age = row.age
   ```
4. **Batch your operations** — Send data in batches of 500–1000 rows per query for optimal throughput

### How to export graph data

Use Cypher queries to export data:

```cypher
// Export all nodes
MATCH (n) RETURN n

// Export specific types
MATCH (p:Person) RETURN p.name, p.age

// Export relationships
MATCH (a)-[r]->(b) RETURN a, type(r), r, b
```

For large datasets, paginate with `SKIP` and `LIMIT`:

```cypher
MATCH (n:Person) RETURN n ORDER BY n.name SKIP 0 LIMIT 1000
MATCH (n:Person) RETURN n ORDER BY n.name SKIP 1000 LIMIT 1000
```

---

## Client Library Errors

### "Module not found" or import errors

- Ensure the client library is installed: `pip install falkordb`, `npm install falkordb`, etc.
- Check you're using the correct package name (e.g., `falkordb`, not `redis`)
- Verify your Python/Node.js version meets the minimum requirements

### "Connection refused" or "ECONNREFUSED"

- The FalkorDB instance may not be running or reachable
- Check host, port, and TLS settings
- Ensure no firewall is blocking the connection

### Serialization / type errors

- FalkorDB returns graph-specific types (nodes, relationships, paths). Use the client library's result parsing methods
- For numbers, ensure you use `toInteger()` or `toFloat()` in Cypher when loading string data

---

## Browser UI

### FalkorDB Browser is not loading

1. **Check the port** — The browser UI typically runs on port `3000`. Ensure it's accessible
2. **Browser compatibility** — Use a modern browser (Chrome, Firefox, Edge). Safari may have limited support
3. **Clear cache** — Try clearing browser cache or opening in an incognito window
4. **Check the URL** — Ensure you're using the correct URL from your Cloud dashboard
5. **Network issues** — If behind a VPN or proxy, ensure port 3000 is allowed

---

## Limits

### Maximum nodes and relationships

FalkorDB is designed to handle large graphs. Practical limits depend on your instance's available memory:

- Each node and relationship consumes memory proportional to the number of properties
- Monitor your instance's memory usage in the Cloud dashboard
- Scale up your instance if approaching memory limits

### Query timeout

- FalkorDB has a configurable query timeout to prevent runaway queries
- If a query times out, optimize it (add indexes, limit scope, simplify pattern)
- Contact support if you need to adjust timeout settings for your Cloud instance

### Max properties per node/relationship

There is no hard limit on the number of properties, but keep them reasonable for performance. Store large text or binary data externally and reference it by URL or ID.

---

## Backup & Recovery

### How to back up my graph

**For FalkorDB Cloud:**
- Cloud instances include automated backups managed by the platform
- Check your Cloud dashboard for backup schedules and restore options

**For self-hosted:**
- FalkorDB persists data using RDB/AOF (Redis persistence mechanisms)
- Back up the RDB file (`dump.rdb`) or use the `BGSAVE` command
- For point-in-time recovery, enable AOF persistence

### How to restore from backup

**For FalkorDB Cloud:**
- Use the restore feature in the Cloud dashboard
- Contact support for assistance with specific restore scenarios

**For self-hosted:**
- Stop the FalkorDB server
- Replace the RDB file with your backup
- Restart the server

---

## Support

### How to get help

| Channel            | Details                                                     |
|--------------------|-------------------------------------------------------------|
| **Documentation**  | [docs.falkordb.com](https://docs.falkordb.com/)             |
| **Discord**        | [discord.gg/falkordb](https://discord.gg/falkordb)          |
| **Email**          | [support@falkordb.com](mailto:support@falkordb.com)         |
| **GitHub Issues**  | [github.com/FalkorDB/FalkorDB](https://github.com/FalkorDB/FalkorDB/issues) |

### When contacting support, include:

1. **Instance details** — Cloud region, instance ID, plan
2. **Error messages** — Full error text and stack traces
3. **Steps to reproduce** — Exact queries or code that triggers the issue
4. **Client library and version** — e.g., `falkordb` Python 1.0.5
5. **Timestamps** — When the issue started or when it occurs

---

## Quick Reference

| Question                        | Answer / Action                                    |
|---------------------------------|----------------------------------------------------|
| Can't connect                   | Check host, port, password, TLS                    |
| Slow queries                    | Add indexes, use PROFILE, add LIMIT                |
| Import CSV data                 | Parse client-side, use UNWIND with batch queries   |
| Export data                     | MATCH + RETURN queries with SKIP/LIMIT pagination  |
| Browser not loading             | Check port 3000, clear cache, try incognito        |
| Query timed out                 | Optimize query, add indexes, limit path depth      |
| Need to reset password          | Cloud dashboard → instance settings                |
| Need help                       | Discord, support@falkordb.com, GitHub Issues       |

---

## Further Reading

- [FalkorDB Documentation](https://docs.falkordb.com/)
- [Cypher Cheat Sheet](./cypher-cheat-sheet.md)
- [Indexing & Performance Tips](./indexing-performance-tips.md)
- [Client Libraries Quick Start](./client-libraries-quickstart.md)
- [FalkorDB Discord](https://discord.gg/falkordb)
