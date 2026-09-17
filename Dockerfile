# Lightweight Python runtime for the FastAPI application.
FROM python:3.13-slim

# All following commands run inside /app in the container.
WORKDIR /app

# Copy dependency definition first.
# This allows Docker to reuse the dependency layer when application code changes.
COPY pyproject.toml .

# Install the application dependencies.
RUN pip install --no-cache-dir .

# Copy the application source code and migrations.
COPY app ./app
COPY migrations ./migrations
COPY alembic.ini .
COPY main.py .

# Document the port used by FastAPI.
EXPOSE 8000

# Production server command.
# No --reload: containers are immutable deployment units.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]