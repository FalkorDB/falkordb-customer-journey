# FalkorDB Customer Journey

A curated learning path and engagement framework that guides FalkorDB users from their first database to production-ready graph applications.

> **This README evolves as the project grows.** New resources and messages will be reflected here as they are added.

---

## Purpose

This project provides FalkorDB users with a **clear, structured learning path** that accompanies them along their journey — from initial sign-up and first query, through best practices and advanced features, all the way to production-scale graph applications.

It contains two pillars:

1. **Resources** — Educational guides, cheat sheets, and best practices that help users learn FalkorDB at their own pace.
2. **Messages** — Lifecycle-driven communications that proactively reach users at the right moment with the right guidance.

---

## Resources

Step-by-step guides and reference material organized by learning stage:

### Getting Started

| Resource | Description |
|----------|-------------|
| [Your First Graph Guide](resources/your-first-graph-guide.md) | Build a complete graph from scratch using a movie database example |
| [FalkorDB Cloud Getting Started](resources/falkordb-cloud-getting-started.md) | Connect to FalkorDB Cloud and run your first queries |
| [Client Libraries Quick Start](resources/client-libraries-quickstart.md) | Install and connect with Python, Node.js, Java, and more |

### Core Skills

| Resource | Description |
|----------|-------------|
| [Cypher Cheat Sheet](resources/cypher-cheat-sheet.md) | Quick-reference for Cypher query syntax — nodes, relationships, filtering, aggregation |
| [Data Modeling Guide](resources/data-modeling-guide.md) | Design effective graph schemas and structure data for performance |
| [Parameterized Queries](resources/parameterized-queries.md) | Best practice for safe, cacheable, and clean Cypher queries |

### Performance & Scale

| Resource | Description |
|----------|-------------|
| [Indexing & Performance Tips](resources/indexing-performance-tips.md) | Indexes, query optimization, bulk loading, and memory considerations |
| [Use Case Examples](resources/use-case-examples.md) | Real-world graph modeling patterns — social networks, recommendations, and more |

### Advanced

| Resource | Description |
|----------|-------------|
| [GraphRAG Getting Started](resources/graphrag-getting-started.md) | Build AI-powered Q&A systems using FalkorDB's GraphRAG SDK |
| [FAQ & Troubleshooting](resources/faq-troubleshooting.md) | Common questions, issues, and solutions for FalkorDB Cloud |

---

## Messages

Lifecycle messages that engage users at key moments in their journey:

| Stage | Message | Trigger |
|-------|---------|---------|
| **Day 0** | [Welcome Message](messages/welcome_message_v1.md) | First database created |
| **Day 0** | [Onboarding Message](messages/onboarding_message_v1.md) | Immediately on DB creation |
| **Day 1–2** | [Support Contact](messages/support_contact_v1.md) | Part of onboarding sequence |
| **Day 3–5** | [Tips & Best Practices](messages/tips_best_practices_v1.md) | Proactive to all new users |
| **On Event** | [First Query Celebration](messages/first_query_celebration_v1.md) | User runs their first query |
| **Day 7+** | [Inactivity Check-In](messages/inactivity_checkin_v1.md) | No activity for 7 days |
| **Day 7–10** | [GraphRAG Introduction](messages/graphrag_introduction_v1.md) | Proactive engagement |
| **Day 14–21** | [Feedback Request](messages/feedback_request_v1.md) | Active user running queries |
| **Day 30** | [Churn Prevention](messages/churn_prevention_v1.md) | No login for 30 days |
| **Usage-based** | [Upgrade & Scale Nudge](messages/upgrade_scale_nudge_v1.md) | Nearing resource limits |

---

## Contributing

To add a new resource or message:

1. Create a `.md` file in the appropriate directory (`resources/` or `messages/`).
2. Follow the formatting style of existing documents.
3. Update this README to include the new entry.
4. Open a pull request for review.

---

## Further Reading

- [FalkorDB Documentation](https://docs.falkordb.com/)
- [Cypher Reference](https://docs.falkordb.com/cypher/)
- [FalkorDB GitHub](https://github.com/FalkorDB)
