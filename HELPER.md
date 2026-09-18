## Local Development

# Create and activate a virtual environment:
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies:
pip install -e ".[dev]"

# Create the environment file:
Copy-Item .env.example .env

# Run database migrations:
alembic upgrade head

# Seed the development user:
python -m app.database.seed

# Start the API:
uvicorn main:app --reload

# Swagger:
http://localhost:8000/docs


## Tests

# Run the deterministic test suite:
pytest -v

# Run AI evaluations separately:
python -m evals.run_evals


## Docker

# Build and start the local environment:
docker compose up --build

# Database migrations can be executed inside the application container:
docker compose run --rm api alembic upgrade head