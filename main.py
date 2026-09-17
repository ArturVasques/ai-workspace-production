"""
AI Workspace application entry point.

Responsibilities:
- configure application-wide infrastructure.
- manage startup/shutdown resources through FastAPI lifespan.
- register HTTP routers.

Business logic must not be implemented in this file.
"""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.documents import router as documents_router

from app.api.health import router as health_router
from app.core.logging import configure_logging, get_logger
from app.database.connection import (
    close_database_pool,
    open_database_pool,
)

configure_logging()
logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage infrastructure resources for the application lifecycle."""

    logger.info("application_starting")

    await open_database_pool()

    logger.info("application_started")

    yield

    logger.info("application_stopping")

    await close_database_pool()

    logger.info("application_stopped")


app = FastAPI(
    title="AI Workspace API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(chat_router)
app.include_router(documents_router)