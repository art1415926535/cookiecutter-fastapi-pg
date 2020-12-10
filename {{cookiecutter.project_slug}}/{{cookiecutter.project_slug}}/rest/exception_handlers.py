from fastapi import exception_handlers

from {{cookiecutter.project_slug}}.logger import get_logger


log = get_logger()


async def http_exception_handler(request, exc):
    log_func = log.warning
    if exc.status_code >= 500:
        log_func = log.error
    log_func(
        "server exception", status_code=exc.status_code, detail=exc.detail
    )
    return await exception_handlers.http_exception_handler(request, exc)


async def validation_exception_handler(request, exc):
    log.warning("validation exception", detail=exc.errors(), body=exc.body)
    return await exception_handlers.request_validation_exception_handler(
        request, exc
    )
