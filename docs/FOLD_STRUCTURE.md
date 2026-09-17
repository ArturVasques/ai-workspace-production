ai-workspace-production/
│
├── app/
│   ├── api/                 # HTTP boundary / FastAPI routers
│   ├── agents/              # Agent definitions
│   ├── auth/                # Authentication + authorization
│   ├── core/                # Config, logging, shared infrastructure
│   ├── database/            # Pool, DB lifecycle
│   ├── models/              # Database models/entities
│   ├── repositories/        # PostgreSQL access
│   ├── schemas/             # Pydantic API/AI contracts
│   ├── services/
│   │   ├── ai/              # Model/Agent execution
│   │   ├── rag/             # Retrieval + ingestion
│   │   └── documents/
│   ├── tools/               # Agent tools
│   └── workers/             # Background processing
│
├── migrations/              # Alembic DB migrations
├── tests/
│   ├── unit/
│   └── integration/
├── evals/                   # AI quality evaluation
├── docs/
│   └── ARCHITECTURE.md
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── .env.example
├── pyproject.toml
└── README.md