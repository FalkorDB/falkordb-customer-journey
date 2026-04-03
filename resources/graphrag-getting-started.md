# Getting Started with FalkorDB GraphRAG SDK

> **⚠️ DRAFT** — This document is a work in progress and has not been finalized for general availability.

Build AI-powered question-answering systems using FalkorDB's GraphRAG SDK. This guide walks you through setup, configuration, and your first natural language query over a knowledge graph.

---

## What is GraphRAG?

**Retrieval-Augmented Generation (RAG)** enhances LLM responses by retrieving relevant data before generating answers. Traditional RAG uses vector search over flat document chunks.

**GraphRAG** takes this further by using a **knowledge graph** as the retrieval layer:

| Feature              | Traditional RAG         | GraphRAG                       |
|----------------------|-------------------------|--------------------------------|
| Data structure       | Flat document chunks    | Interconnected graph of entities|
| Retrieval            | Vector similarity       | Graph traversal + Cypher       |
| Context quality      | Keyword/semantic match  | Relationship-aware context     |
| Multi-hop reasoning  | Limited                 | Native (traverse relationships)|
| Explainability       | Low                     | High (see the Cypher query)    |

GraphRAG excels at questions that require understanding **relationships** between entities — e.g., "Which customers bought products also bought by Alice?" or "What's the connection between entity X and entity Y?"

---

## Prerequisites

- **Python 3.9+**
- **A running FalkorDB instance** — [FalkorDB Cloud](https://app.falkordb.cloud) or self-hosted
- **An LLM API key** — OpenAI, Google Gemini, Groq, or any LiteLLM-compatible provider
- **A populated graph** — The SDK can extract ontology from an existing graph

---

## Installation

```bash
pip install graphrag_sdk
```

This also installs the `falkordb` Python client and `litellm` for multi-provider LLM support.

---

## Step-by-Step Walkthrough

### 1. Connect to FalkorDB

First, establish a connection to your FalkorDB instance:

```python
import os
from falkordb import FalkorDB

db = FalkorDB(
    host=os.getenv("FALKORDB_HOST", "localhost"),
    port=os.getenv("FALKORDB_PORT", 6379),
    username=os.getenv("FALKORDB_USERNAME"),
    password=os.getenv("FALKORDB_PASSWORD")
)

graph = db.select_graph("my_graph")
```

For FalkorDB Cloud, set the environment variables to your cloud instance's connection details.

### 2. Extract the Ontology

The ontology defines the schema of your knowledge graph — what node labels, relationship types, and properties exist. You can extract it automatically from an existing graph:

```python
from graphrag_sdk.ontology import Ontology

ontology = Ontology.from_kg_graph(graph)
```

This inspects your graph and builds a schema that the LLM uses to generate accurate Cypher queries.

### 3. Configure the LLM Model

The SDK uses LiteLLM for multi-provider support. Set your API key as an environment variable:

```bash
# For OpenAI
export OPENAI_API_KEY="sk-..."

# For Google Gemini
export GEMINI_API_KEY="..."

# For Groq
export GROQ_API_KEY="..."
```

Then configure the model in Python:

```python
from graphrag_sdk.models.litellm import LiteModel
from graphrag_sdk.model_config import KnowledgeGraphModelConfig

model = LiteModel()  # Uses default model, or pass model="gpt-4o" etc.
model_config = KnowledgeGraphModelConfig.with_model(model)
```

### 4. Create the KnowledgeGraph Instance

Bring everything together — the graph connection, ontology, and model configuration:

```python
from graphrag_sdk import KnowledgeGraph

kg = KnowledgeGraph(
    name="my_graph",
    model_config=model_config,
    ontology=ontology,
    host=os.getenv("FALKORDB_HOST", "localhost"),
    port=os.getenv("FALKORDB_PORT", 6379),
    username=os.getenv("FALKORDB_USERNAME"),
    password=os.getenv("FALKORDB_PASSWORD")
)
```

### 5. Start a Chat Session and Ask Questions

Create a chat session and send natural language questions. The SDK translates your question into a Cypher query, runs it, and returns a natural language answer:

```python
chat = kg.chat_session()

response = chat.send_message("What products are available?")
print(response["response"])
```

The chat session maintains conversation context, so follow-up questions work naturally.

---

## Full Working Example

```python
import os
from falkordb import FalkorDB
from graphrag_sdk import KnowledgeGraph
from graphrag_sdk.ontology import Ontology
from graphrag_sdk.models.litellm import LiteModel
from graphrag_sdk.model_config import KnowledgeGraphModelConfig

db = FalkorDB(
    host=os.getenv("FALKORDB_HOST", "localhost"),
    port=os.getenv("FALKORDB_PORT", 6379),
    username=os.getenv("FALKORDB_USERNAME"),
    password=os.getenv("FALKORDB_PASSWORD")
)

graph = db.select_graph("my_graph")
ontology = Ontology.from_kg_graph(graph)

model = LiteModel()
model_config = KnowledgeGraphModelConfig.with_model(model)

kg = KnowledgeGraph(
    name="my_graph",
    model_config=model_config,
    ontology=ontology,
    host=os.getenv("FALKORDB_HOST", "localhost"),
    port=os.getenv("FALKORDB_PORT", 6379),
    username=os.getenv("FALKORDB_USERNAME"),
    password=os.getenv("FALKORDB_PASSWORD")
)

chat = kg.chat_session()
response = chat.send_message("What products are available?")
print(response["response"])
```

---

## Key Features

### Ontology Extraction

Automatically discover the schema of your graph — node labels, relationship types, and properties — without manual configuration:

```python
ontology = Ontology.from_kg_graph(graph)
print(ontology)  # View discovered schema
```

### Natural Language to Cypher

The SDK translates natural language questions into Cypher queries using the LLM and your graph's ontology. You can inspect the generated query:

```python
response = chat.send_message("Who are Alice's friends?")
print(response["response"])    # Natural language answer
```

### Multi-Provider LLM Support

Thanks to LiteLLM integration, you can use models from multiple providers:

```python
# OpenAI
model = LiteModel(model="gpt-4o")

# Google Gemini
model = LiteModel(model="gemini/gemini-1.5-pro")

# Groq
model = LiteModel(model="groq/llama-3.1-70b-versatile")
```

### Conversational Context

Chat sessions maintain context, so follow-up questions work naturally:

```python
chat = kg.chat_session()
chat.send_message("Show me all customers in New York")
chat.send_message("Which of them placed orders last month?")  # Understands "them" = NY customers
```

---

## Environment Variables Reference

| Variable            | Description                        | Default     |
|---------------------|------------------------------------|-------------|
| `FALKORDB_HOST`     | FalkorDB server hostname           | `localhost` |
| `FALKORDB_PORT`     | FalkorDB server port               | `6379`      |
| `FALKORDB_USERNAME` | FalkorDB username (Cloud)          | —           |
| `FALKORDB_PASSWORD` | FalkorDB password (Cloud)          | —           |
| `OPENAI_API_KEY`    | OpenAI API key                     | —           |
| `GEMINI_API_KEY`    | Google Gemini API key              | —           |
| `GROQ_API_KEY`      | Groq API key                       | —           |

---

## Further Reading

- [GraphRAG SDK on GitHub](https://github.com/FalkorDB/GraphRAG-SDK)
- [GraphRAG SDK Documentation](https://docs.falkordb.com/genai-tools/graphrag-sdk)
- [FalkorDB Python Client](https://docs.falkordb.com/getting-started/clients.html)
- [FalkorDB Documentation](https://docs.falkordb.com/)
