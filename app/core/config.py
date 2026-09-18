"""
Central application configuration.

All configuration is loaded from environment variables or the local `.env`
file through Pydantic Settings.

Used by:
- database/connection.py for PostgreSQL configuration.
- AI services for model configuration.
- RAG services for retrieval configuration.
- application startup for environment and logging settings.

Production environments should inject these values through the deployment
platform rather than shipping a `.env` file.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed configuration contract for the entire application."""

    # Application
    app_env: str = "development"
    log_level: str = "INFO"

    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-5.6-luna"
    openai_embedding_model: str = "text-embedding-3-small"

    # PostgreSQL
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "ai_workspace_production"
    postgres_user: str = "postgres"
    postgres_password: str

    # RAG
    rag_top_k: int = 5
    rag_max_distance: float = 0.8

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return the application settings singleton.

    Caching avoids repeatedly parsing environment configuration throughout
    the application.
    """
    return Settings()