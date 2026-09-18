# Lightweight Python runtime for the FastAPI application.
FROM python:3.13-slim

WORKDIR /app

# Copy the package definition and application source before installation.
COPY pyproject.toml .
COPY app ./app

# Install the application and its production dependencies.
RUN pip install --no-cache-dir .

# Runtime files required by the application and Alembic.
COPY migrations ./migrations
COPY alembic.ini .
COPY main.py .

EXPOSE 8000

# Production containers run without development auto-reload.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]