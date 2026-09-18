# AI Workspace Production

Production-oriented AI application built to demonstrate the architecture of a modern AI Engineering system.

The project combines a traditional backend architecture with LLM agents, tool calling, RAG, vector search, structured outputs, multi-tenant security boundaries, testing, evals and containerization.

## Tech Stack

- Python 3.13
- FastAPI
- OpenAI API
- OpenAI Agents SDK
- PostgreSQL
- pgvector
- Alembic
- Pydantic
- psycopg
- pytest
- Docker / Docker Compose
- GitHub Actions

## Architecture

```text
Client
  │
  ▼
FastAPI
  │
  ├── Authentication / AppContext
  │
  ▼
AI Agent
  │
  ├── User Tool ──────────────► PostgreSQL
  │
  └── Knowledge Tool
          │
          ▼
       Embedding
          │
          ▼
     pgvector / HNSW
          │
          ▼
     Relevant chunks
          │
          ▼
        Agent
          │
          ▼
   Structured Output
```

See `HELPER.md` for local development, testing (unit vs. integration),
linting/type-checking and Docker commands, and `docs/ARCHITECTURE.md` for
the full architecture reference.