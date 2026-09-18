ai-workspace-production/
│
├── app/
│   ├── api/                 # HTTP boundary / FastAPI routers + error handlers (errors.py)
│   ├── agents/               # Agent definitions
│   ├── auth/                 # Authentication, authorization, permission constants (permissions.py)
│   ├── core/                 # Config, logging, middleware, event loop, shared infrastructure (middleware.py, event_loop.py)
│   ├── database/              # Pool, DB lifecycle, dev seed
│   ├── repositories/          # PostgreSQL access
│   ├── schemas/                # Pydantic API/AI contracts
│   ├── services/
│   │   ├── ai/                # Model/Agent execution
│   │   ├── rag/                # Retrieval + chunking
│   │   └── documents/          # Ingestion orchestration
│   └── tools/                  # Agent tools
│
├── migrations/               # Alembic DB migrations
├── tests/
│   ├── unit/                  # No database required (see tests/conftest.py)
│   ├── integration/            # Real PostgreSQL/pgvector (see tests/integration/conftest.py)
│   │   └── conftest.py         # Database pool fixture for the integration suite
├── evals/                     # AI quality evaluation
├── docs/
│   ├── ARCHITECTURE.md
│   ├── FOLD_STRUCTURE.md       # This file
│   └── CODESTYLE.md            # Code style and patterns
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt          # Pinned production dependency lock used by Dockerfile
├── .dockerignore
├── .gitignore
├── .env.example
├── pyproject.toml
└── README.md
