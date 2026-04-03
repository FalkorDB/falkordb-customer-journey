# Using WAIT for Write Durability in FalkorDB

Ensure your writes are replicated to replicas before reading them back. The `WAIT` command bridges the gap between FalkorDB's asynchronous replication and the stronger consistency your application may need.

For background on the primary/replica architecture, see [Read & Write Operations](read-write-operations.md).

---

## The Problem — Replication Lag

FalkorDB replicates data from the primary to replicas **asynchronously**. This means there is a small window (typically milliseconds) where a write has been accepted by the primary but hasn't reached the replicas yet.

```
1. App writes to Primary      ✅ Write succeeds
2. App reads from Replica      ❌ Data not there yet (replication lag)
```

If your application writes data and then immediately reads it from a replica (using `GRAPH.RO_QUERY`), the read may return stale results.

---

## The Solution — WAIT

The `WAIT` command blocks until all previous write commands have been acknowledged by a specified number of replicas, or until a timeout is reached.

```
WAIT <num_replicas> <timeout_ms>
```

| Parameter | Description |
|-----------|-------------|
| `num_replicas` | Minimum number of replicas that must acknowledge the write |
| `timeout_ms` | Maximum time to wait in milliseconds (0 = wait forever) |

**Returns:** The number of replicas that actually acknowledged the write. Always check that this value is ≥ the number you requested.

### How It Works

```
1. App writes to Primary           ✅ Write succeeds
2. App calls WAIT 1 5000           ⏳ Blocks until 1 replica confirms (up to 5s)
3. WAIT returns 1                  ✅ Replica has the data
4. App reads from Replica           ✅ Data is there
```

### Important Notes

- `WAIT` does **not** make FalkorDB strongly consistent — it improves real-world data safety but doesn't guarantee it during failovers.
- `WAIT` applies to **all writes** made by the current connection before the `WAIT` call, not just the last one.
- On a standalone instance with no replicas, `WAIT` returns `0` immediately.
- A timeout of `0` means block forever — use with caution.

---

## Code Examples — CLI

### Write Then Wait

```shell
# Step 1: Write data on the primary
GRAPH.QUERY social "CREATE (p:Person {name: 'Alice', age: 30})"

# Step 2: Wait for 1 replica to acknowledge, with a 5-second timeout
WAIT 1 5000
# Returns: (integer) 1  — 1 replica confirmed

# Step 3: Now safe to read from the replica
GRAPH.RO_QUERY social "MATCH (p:Person {name: 'Alice'}) RETURN p.name, p.age"
```

### Bulk Write Then Wait

```shell
# Perform multiple writes
GRAPH.QUERY social "UNWIND $people AS p CREATE (:Person {name: p.name, age: p.age})" "CYPHER people=[{name:'Bob',age:25},{name:'Carol',age:35}]"
GRAPH.QUERY social "MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'}) CREATE (a)-[:KNOWS]->(b)"

# Single WAIT covers ALL preceding writes on this connection
WAIT 1 5000

# Safe to read from replicas
GRAPH.RO_QUERY social "MATCH (p:Person) RETURN p.name ORDER BY p.name"
```

### Handling Timeout

```shell
GRAPH.QUERY social "CREATE (p:Person {name: 'Dave'})"

# Ask for 2 replicas but only 1 exists — will timeout
WAIT 2 3000
# Returns: (integer) 1  — only 1 replica confirmed
# Your code should check: 1 < 2, so replication target was NOT met
```

---

## Code Examples — Python

The `WAIT` command is issued through the underlying Redis connection, not the graph object.

### Setup

```bash
pip install FalkorDB
```

### Write, Wait, Read

```python
from falkordb import FalkorDB

db = FalkorDB(host='localhost', port=6379)
graph = db.select_graph('social')

# Step 1: Write data
graph.query(
    "CREATE (p:Person {name: $name, age: $age})",
    params={"name": "Alice", "age": 30}
)

# Step 2: Wait for 1 replica to acknowledge (5-second timeout)
num_replicas = db.connection.execute_command("WAIT", 1, 5000)
print(f"Replicas confirmed: {num_replicas}")

if num_replicas < 1:
    print("Warning: replication target not met")

# Step 3: Safe to read from a replica
result = graph.ro_query(
    "MATCH (p:Person {name: $name}) RETURN p.name, p.age",
    params={"name": "Alice"}
)
for row in result.result_set:
    print(row)
```

### Helper Function

```python
def write_and_wait(graph, db, query, params=None, replicas=1, timeout_ms=5000):
    """
    Execute a write query and wait for replication.
    Raises an exception if the replication target is not met.
    """
    result = graph.query(query, params=params)

    confirmed = db.connection.execute_command("WAIT", replicas, timeout_ms)
    if confirmed < replicas:
        raise RuntimeError(
            f"Replication target not met: {confirmed}/{replicas} replicas confirmed"
        )

    return result


# Usage
write_and_wait(
    graph, db,
    "MERGE (p:Person {name: $name}) SET p.age = $age",
    params={"name": "Alice", "age": 31},
    replicas=1,
    timeout_ms=5000
)
```

---

## Code Examples — Node.js

The `WAIT` command is issued through the underlying Redis client, not the graph object.

### Setup

```bash
npm install falkordb
```

### Write, Wait, Read

```javascript
import { FalkorDB } from 'falkordb';

const db = await FalkorDB.connect({
    socket: { host: 'localhost', port: 6379 }
});

const graph = db.selectGraph('social');

// Step 1: Write data
await graph.query(
    "CREATE (p:Person {name: $name, age: $age})",
    { params: { name: "Alice", age: 30 } }
);

// Step 2: Wait for 1 replica to acknowledge (5-second timeout)
const numReplicas = await db.connection.sendCommand(["WAIT", "1", "5000"]);
console.log(`Replicas confirmed: ${numReplicas}`);

if (numReplicas < 1) {
    console.warn("Warning: replication target not met");
}

// Step 3: Safe to read from a replica
const result = await graph.roQuery(
    "MATCH (p:Person {name: $name}) RETURN p.name, p.age",
    { params: { name: "Alice" } }
);
console.log(result.data);

db.close();
```

### Helper Function

```javascript
async function writeAndWait(graph, db, query, options = {}) {
    const { params, replicas = 1, timeoutMs = 5000 } = options;

    const result = await graph.query(query, { params });

    const confirmed = await db.connection.sendCommand([
        "WAIT",
        String(replicas),
        String(timeoutMs)
    ]);

    if (confirmed < replicas) {
        throw new Error(
            `Replication target not met: ${confirmed}/${replicas} replicas confirmed`
        );
    }

    return result;
}

// Usage
await writeAndWait(graph, db,
    "MERGE (p:Person {name: $name}) SET p.age = $age",
    { params: { name: "Alice", age: 31 }, replicas: 1, timeoutMs: 5000 }
);
```

---

## When to Use WAIT

| Scenario | Use WAIT? | Why |
|----------|-----------|-----|
| Critical write followed by immediate read from replica | ✅ Yes | Prevents stale reads |
| User-facing write (e.g., profile update) then display | ✅ Yes | User expects to see their change immediately |
| Background batch import | ❌ No | Eventual consistency is fine; WAIT would slow the import |
| All reads go to the primary | ❌ No | No replication lag when reading from the primary |
| Write-heavy pipeline with no immediate read | ❌ No | Let replication happen asynchronously |
| Financial or transactional data requiring confirmation | ✅ Yes | Data safety is critical |

---

## Best Practices

| ✅ Do | ❌ Don't |
|-------|----------|
| Check the return value of `WAIT` against your target | Assume `WAIT` always succeeds |
| Use a reasonable timeout (e.g., 5000ms) | Use `WAIT 1 0` (infinite) in production — can block forever |
| Group multiple writes before a single `WAIT` | Call `WAIT` after every individual write |
| Use `WAIT` only when you need to read back from replicas | Call `WAIT` on every write regardless of read pattern |
| Log or alert when `WAIT` returns fewer replicas than expected | Silently ignore replication failures |

---

## Quick Reference

| Operation | CLI | Python | Node.js |
|-----------|-----|--------|---------|
| **Write** | `GRAPH.QUERY graph "..."` | `graph.query("...")` | `await graph.query("...")` |
| **Wait** | `WAIT 1 5000` | `db.connection.execute_command("WAIT", 1, 5000)` | `await db.connection.sendCommand(["WAIT", "1", "5000"])` |
| **Read (replica)** | `GRAPH.RO_QUERY graph "..."` | `graph.ro_query("...")` | `await graph.roQuery("...")` |

---

## Further Reading

- [Redis WAIT Command Reference](https://redis.io/docs/latest/commands/wait/)
- [Read & Write Operations Guide](read-write-operations.md)
- [Parameterized Queries Best Practice](parameterized-queries.md)
- [FalkorDB Cloud — High Availability](https://docs.falkordb.com/cloud/pro-tier.html)
- [FalkorDB Documentation](https://docs.falkordb.com/)
