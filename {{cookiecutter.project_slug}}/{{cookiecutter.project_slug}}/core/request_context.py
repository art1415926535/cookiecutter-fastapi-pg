import contextlib
from typing import Callable

import sentry_sdk
from fastapi import Request
from structlog.contextvars import bind_contextvars, clear_contextvars


@contextlib.contextmanager
def _bind(request_id):
    bind_contextvars(request_id=request_id)
    yield
    clear_contextvars()


async def add_log_context(request: Request, call_next: Callable):
    """Add X-Request-ID header value to logs."""
    request_id = request.headers.get("X-Request-ID")

    with _bind(request_id=request_id), sentry_sdk.configure_scope() as scope:
        scope.set_context("request_id", request_id)
        return await call_next(request)
