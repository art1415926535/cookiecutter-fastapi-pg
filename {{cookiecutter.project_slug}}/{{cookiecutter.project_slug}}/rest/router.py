from typing import Protocol

from fastapi import APIRouter

from . import admin, users


class _RouterSettings(Protocol):
    fastapi_admin_route_prefix: str


def get_router(settings: _RouterSettings) -> APIRouter:
    """Create router."""
    router = APIRouter()
    router.include_router(
        admin.router,
        prefix=f"/{settings.fastapi_admin_route_prefix.lstrip('/')}",
        tags=["admin"],
    )
    router.include_router(users.router, prefix="/users", tags=["user"])

    return router
