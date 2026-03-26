# FalkorDB Client Libraries — Quick Start

Official client libraries for connecting to FalkorDB from your application. Each example shows installation, connection, creating a node, and running a query.

For full documentation, see [docs.falkordb.com/getting-started/clients.html](https://docs.falkordb.com/getting-started/clients.html).

---

## Python

**Package:** [falkordb](https://pypi.org/project/falkordb/)

### Install

```bash
pip install falkordb
```

### Connect and Query

```python
from falkordb import FalkorDB

# Connect (for Cloud, set host, port, password, and ssl=True)
db = FalkorDB(
    host="localhost",
    port=6379,
    password="your_password",
    ssl=True  # Required for FalkorDB Cloud
)

# Select a graph
graph = db.select_graph("my_graph")

# Create a node
graph.query("CREATE (p:Person {name: 'Alice', age: 30})")

# Query
result = graph.query("MATCH (p:Person) RETURN p.name, p.age")
for record in result.result_set:
    print(record)
```

---

## Node.js

**Package:** [falkordb](https://www.npmjs.com/package/falkordb)

### Install

```bash
npm install falkordb
```

### Connect and Query

```javascript
import { FalkorDB } from 'falkordb';

async function main() {
  // Connect (for Cloud, set host, port, password, and tls)
  const db = await FalkorDB.connect({
    socket: {
      host: 'localhost',
      port: 6379,
      tls: true  // Required for FalkorDB Cloud
    },
    password: 'your_password'
  });

  // Select a graph
  const graph = db.selectGraph('my_graph');

  // Create a node
  await graph.query("CREATE (p:Person {name: 'Alice', age: 30})");

  // Query
  const result = await graph.query("MATCH (p:Person) RETURN p.name, p.age");
  result.data.forEach(record => {
    console.log(record);
  });

  await db.close();
}

main();
```

---

## Java

**Package:** [jfalkordb](https://central.sonatype.com/artifact/com.falkordb/jfalkordb)

### Maven Dependency

```xml
<dependency>
    <groupId>com.falkordb</groupId>
    <artifactId>jfalkordb</artifactId>
    <version>LATEST</version>
</dependency>
```

### Connect and Query

```java
import com.falkordb.FalkorDB;
import com.falkordb.Graph;
import com.falkordb.ResultSet;

public class Example {
    public static void main(String[] args) {
        // Connect (for Cloud, configure SSL and password)
        FalkorDB db = FalkorDB.driver()
            .host("localhost")
            .port(6379)
            .password("your_password")
            .ssl(true)  // Required for FalkorDB Cloud
            .build();

        // Select a graph
        Graph graph = db.graph("my_graph");

        // Create a node
        graph.query("CREATE (p:Person {name: 'Alice', age: 30})");

        // Query
        ResultSet result = graph.query("MATCH (p:Person) RETURN p.name, p.age");
        while (result.hasNext()) {
            System.out.println(result.next());
        }

        db.close();
    }
}
```

---

## Go

**Package:** [falkordb-go](https://github.com/FalkorDB/falkordb-go)

### Install

```bash
go get github.com/FalkorDB/falkordb-go
```

### Connect and Query

```go
package main

import (
	"fmt"
	"github.com/FalkorDB/falkordb-go"
)

func main() {
	// Connect (for Cloud, configure TLS and password)
	db, err := falkordb.Connect(
		falkordb.WithHost("localhost"),
		falkordb.WithPort(6379),
		falkordb.WithPassword("your_password"),
		falkordb.WithTLS(true), // Required for FalkorDB Cloud
	)
	if err != nil {
		panic(err)
	}
	defer db.Close()

	// Select a graph
	graph := db.SelectGraph("my_graph")

	// Create a node
	graph.Query("CREATE (p:Person {name: 'Alice', age: 30})")

	// Query
	result, _ := graph.Query("MATCH (p:Person) RETURN p.name, p.age")
	for result.Next() {
		record := result.Record()
		fmt.Println(record)
	}
}
```

---

## Rust

**Package:** [falkordb](https://crates.io/crates/falkordb)

### Install

```bash
cargo add falkordb
```

### Connect and Query

```rust
use falkordb::FalkorDB;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Connect (for Cloud, configure TLS and password)
    let db = FalkorDB::connect(
        "falkor://your_password@localhost:6379"
    ).await?;

    // Select a graph
    let mut graph = db.select_graph("my_graph");

    // Create a node
    graph.query("CREATE (p:Person {name: 'Alice', age: 30})").execute().await?;

    // Query
    let mut result = graph
        .query("MATCH (p:Person) RETURN p.name, p.age")
        .execute()
        .await?;

    while let Some(record) = result.next() {
        println!("{:?}", record);
    }

    Ok(())
}
```

---

## C# (.NET)

**Package:** [NFalkorDB](https://www.nuget.org/packages/NFalkorDB)

### Install

```bash
dotnet add package NFalkorDB
```

### Connect and Query

```csharp
using NFalkorDB;

// Connect (for Cloud, configure SSL and password)
var db = FalkorDB.Connect(
    host: "localhost",
    port: 6379,
    password: "your_password",
    ssl: true  // Required for FalkorDB Cloud
);

// Select a graph
var graph = db.SelectGraph("my_graph");

// Create a node
graph.Query("CREATE (p:Person {name: 'Alice', age: 30})");

// Query
var result = graph.Query("MATCH (p:Person) RETURN p.name, p.age");
foreach (var record in result)
{
    Console.WriteLine(record);
}
```

---

## PHP

**Package:** [falkordb-php](https://github.com/FalkorDB/falkordb-php)

### Install

Install via Composer from GitHub:

```bash
composer require falkordb/falkordb-php
```

### Connect and Query

```php
<?php
require_once 'vendor/autoload.php';

use FalkorDB\FalkorDB;

// Connect (for Cloud, configure SSL and password)
$db = FalkorDB::connect([
    'host' => 'localhost',
    'port' => 6379,
    'password' => 'your_password',
    'ssl' => true  // Required for FalkorDB Cloud
]);

// Select a graph
$graph = $db->selectGraph('my_graph');

// Create a node
$graph->query("CREATE (p:Person {name: 'Alice', age: 30})");

// Query
$result = $graph->query("MATCH (p:Person) RETURN p.name, p.age");
foreach ($result as $record) {
    print_r($record);
}
```

---

## OGM (Object-Graph Mapping) Libraries

For a more structured, model-driven approach, FalkorDB offers OGM libraries:

| Language | Library                | Link                                                    |
|----------|------------------------|---------------------------------------------------------|
| Python   | FalkorDB OGM (Python)  | [GitHub](https://github.com/FalkorDB/falkordb-py)       |
| Go       | FalkorDB OGM (Go)      | [GitHub](https://github.com/FalkorDB/falkordb-go)       |
| Java     | Spring Data FalkorDB   | [GitHub](https://github.com/FalkorDB/spring-data-falkordb) |

OGM libraries let you define graph schemas as classes/structs and interact with the database using native language objects instead of raw Cypher.

---

## Connection Tips for FalkorDB Cloud

When connecting to a FalkorDB Cloud instance:

1. **Host** — Use the hostname provided in your Cloud dashboard
2. **Port** — Use the port shown in the dashboard (typically `6379` or a custom port)
3. **Password** — Use the password from your instance credentials
4. **TLS/SSL** — Always enable TLS (`ssl=True`, `tls: true`) for Cloud connections
5. **Username** — Set if your instance requires authentication with a username

---

## Further Reading

- [Client Libraries Documentation](https://docs.falkordb.com/getting-started/clients.html)
- [Cypher Query Language](https://docs.falkordb.com/cypher/)
- [FalkorDB Documentation](https://docs.falkordb.com/)
