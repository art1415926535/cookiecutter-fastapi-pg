from typing import Protocol

from fastapi import APIRouter

from . import admin, items


class _RouterSettings(Protocol):
    fastapi_admin_route_prefix: str
    docs_admin_route_include_in_schema: bool


def get_router(settings: _RouterSettings) -> APIRouter:
    """Create router."""
    router = APIRouter()
    router.include_router(
        admin.router,
        include_in_schema=settings.docs_admin_route_include_in_schema,
        prefix=f"/{settings.fastapi_admin_route_prefix.lstrip('/')}",
        tags=["admin"],
    )
    router.include_router(items.router, prefix="/items")

    return router
