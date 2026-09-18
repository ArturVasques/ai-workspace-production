## Local Development

# Create and activate a virtual environment:
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies:
pip install -e ".[dev]"

# Create the environment file:
Copy-Item .env.example .env

# Set APP_ENV (required, no default) and a real OPENAI_API_KEY in .env.

# Run database migrations:
alembic upgrade head

# Seed the development user:
python -m app.database.seed

# Start the API (with auto-reload):
uvicorn main:app --reload

# Start the API on Windows WITHOUT --reload:
# uvicorn's default loop returns Python's ProactorEventLoop on Windows when
# not running inside a --reload subprocess, and psycopg cannot run in async
# mode on ProactorEventLoop ("Psycopg cannot use the 'ProactorEventLoop' to
# run in async mode"). app/core/event_loop.py provides a loop factory that
# uses SelectorEventLoop on Windows (and the normal default elsewhere), wired
# in via uvicorn's --loop option:
uvicorn main:app --loop app.core.event_loop:loop_factory

# Swagger:
http://localhost:8000/docs


## Tests

# Unit tests: deterministic, no database required.
pytest tests/unit -v

# Integration tests: require a reachable PostgreSQL + pgvector database
# (the one configured in .env) with migrations applied.
pytest tests/integration -v

# Coverage report:
pytest --cov=app --cov-report=term-missing

# Run AI evaluations separately (spends OpenAI credit):
python -m evals.run_evals


## Code Quality

# Lint:
ruff check .

# Format check:
ruff format --check .
ruff format .          # apply formatting

# Type check:
mypy


## Docker

# Build and start the local environment:
docker compose up --build

# Database migrations can be executed inside the application container:
docker compose run --rm api alembic upgrade head

# Dockerfile layering: requirements.txt (a pinned dependency lock generated
# from the dev venv via `pip freeze`) is installed BEFORE the application
# source is copied in, so an application code change only rebuilds the
# small final layer instead of reinstalling every dependency. The image
# runs as a non-root user and exposes a HEALTHCHECK against /health/live.
# Regenerate requirements.txt after changing pyproject.toml dependencies
# (see the comment at the top of requirements.txt for the exact command).
