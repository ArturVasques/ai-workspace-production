"""
FastAPI authentication boundary.

This module converts authenticated HTTP identity into trusted AppContext.

Development currently uses explicit headers so the complete architecture can
run locally without requiring an external identity provider.

Production:
Replace the development implementation with Entra ID JWT validation while
keeping AppContext and all downstream agents/tools unchanged.

Security:
Development header authentication must never be enabled in production.
"""

from uuid import UUID

from fastapi import Header, HTTPException, status

from app.auth.context import AppContext
from app.core.config import get_settings

settings = get_settings()


async def get_app_context(
    x_user_id: UUID | None = Header(default=None),
    x_tenant_id: UUID | None = Header(default=None),
) -> AppContext:
    """
    Build trusted application context for a local development request.

    Production implementations must derive identity from a validated token,
    never from caller-controlled identity headers.
    """

    if settings.app_env != "development":
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Production identity provider is not configured",
        )

    if x_user_id is None or x_tenant_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Development identity headers are required",
        )

    return AppContext(
        user_id=x_user_id,
        tenant_id=x_tenant_id,
        permissions=frozenset(
            {
                "knowledge:read",
                "documents:create",
            }
        ),
    )