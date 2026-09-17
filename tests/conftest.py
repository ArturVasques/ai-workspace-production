"""
Pytest configuration for platform-specific async behaviour.

Psycopg async requires a SelectorEventLoop on Windows.
"""

import asyncio
import sys


if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )