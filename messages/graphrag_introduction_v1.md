# GraphRAG Introduction
**Trigger:** Proactive
**Send timing:** Day 7–10 after signup

---

## Subject: Build smarter AI apps with FalkorDB + GraphRAG

---

Hi {First Name},

If you're building AI-powered applications, you'll want to know about **GraphRAG** — Retrieval-Augmented Generation backed by a knowledge graph.

Instead of relying on flat vector search alone, GraphRAG uses the structure and relationships in your graph to give LLMs richer, more accurate context. The result: smarter answers with fewer hallucinations.

### FalkorDB GraphRAG SDK

FalkorDB has an open-source **GraphRAG SDK** that makes it easy to get started:

- 🔄 **Natural language to Cypher** — converts user questions into graph queries automatically
- 🤖 **Multi-model support** — works with OpenAI, Gemini, and Groq
- 💬 **Chat sessions over graph data** — build conversational interfaces on top of your knowledge graph

### Get started in minutes

```bash
pip install graphrag_sdk
```

```python
from graphrag_sdk import KnowledgeGraph, Ontology
from graphrag_sdk.models.litellm import LiteModel

model = LiteModel("gpt-4o")
ontology = Ontology.from_json("ontology.json")
kg = KnowledgeGraph("my_graph", model, ontology)
```

### Resources

- 📖 **[GraphRAG SDK Documentation](https://docs.falkordb.com/genai-tools/graphrag-sdk)**
- 🔗 **[GitHub Repository](https://github.com/FalkorDB/GraphRAG-SDK)**

Have questions about integrating GraphRAG into your project? Reply to this message — we'd love to help.

— The FalkorDB Team

---

*You're receiving this because you're a FalkorDB Cloud user.*
