"""
Shared pytest configuration.

The database pool follows the same lifecycle as the production application:
it is opened once for the test session and closed when the session finishes.

Windows requires the Selector event loop for psycopg async support.
"""

import asyncio
import sys

import pytest_asyncio

from app.database.connection import (
    close_database_pool,
    open_database_pool,
)


if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )


@pytest_asyncio.fixture(scope="session", autouse=True)
async def database_pool():
    """Keep the shared database pool alive for the complete test session."""

    await open_database_pool()

    yield

    await close_database_pool()