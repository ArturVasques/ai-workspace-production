"""
Agent tools for authenticated-user information.

Identity is always derived from trusted AppContext instead of model-generated
arguments.

Used by:
- assistant agent when user-specific application data is required.
"""

from agents import RunContextWrapper, function_tool

from app.auth.context import AppContext
from app.repositories.user_repository import get_user_by_id


@function_tool
async def get_my_profile(
    context: RunContextWrapper[AppContext],
) -> str:
    """Get the authenticated user's application profile."""

    user = await get_user_by_id(
        user_id=context.context.user_id,
        tenant_id=context.context.tenant_id,
    )

    if user is None:
        return "Authenticated user profile was not found."

    return (
        f"Name: {user.name}\n"
        f"Email: {user.email}"
    )