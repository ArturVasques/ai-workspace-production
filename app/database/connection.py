"""
PostgreSQL connection infrastructure.

Provides the shared asynchronous connection pool used by repositories.

Used by:
- FastAPI lifespan to open and close database connections.
- repositories to acquire PostgreSQL connections.

The API is asynchronous, so database I/O also uses psycopg's
AsyncConnectionPool instead of blocking the event loop with synchronous I/O.
"""

from psycopg_pool import AsyncConnectionPool
from pgvector.psycopg import register_vector_async

from app.core.config import get_settings
from app.core.logging import get_logger

settings = get_settings()
logger = get_logger()


async def configure_connection(connection) -> None:
    """Register pgvector types on every connection created by the pool."""
    await register_vector_async(connection)


pool = AsyncConnectionPool(
    conninfo="",
    kwargs={
        "host": settings.postgres_host,
        "port": settings.postgres_port,
        "dbname": settings.postgres_db,
        "user": settings.postgres_user,
        "password": settings.postgres_password,
    },
    min_size=1,
    max_size=10,
    configure=configure_connection,
    open=False,
)


async def open_database_pool() -> None:
    """Open the shared database connection pool during application startup."""

    await pool.open()
    await pool.wait()

    logger.info(
        "database_pool_started",
        database=settings.postgres_db,
    )


async def close_database_pool() -> None:
    """Close all pooled connections during application shutdown."""

    await pool.close()

    logger.info("database_pool_closed")