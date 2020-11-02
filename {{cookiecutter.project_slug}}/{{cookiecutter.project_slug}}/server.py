from typing import Optional

from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware

from {{cookiecutter.project_slug}} import logger
from {{cookiecutter.project_slug}}.core.app_event_handler import (
    start_app_handler,
    stop_app_handler,
)
from {{cookiecutter.project_slug}}.rest.router import get_router
from {{cookiecutter.project_slug}}.settings import LoggerSettings, ServiceSettings


def get_application(
    settings: Optional[ServiceSettings] = None,
    logger_settings: Optional[LoggerSettings] = None,
):
    """Application factory."""
    if logger_settings is None:
        logger_settings = LoggerSettings()

    logger.configure(logger_settings)

    if settings is None:
        settings = ServiceSettings()

    docs_enabled = settings.docs_enabled
    application = FastAPI(
        title=settings.app_title,
        version=settings.app_version,
        debug=settings.fastapi_debug,
        openapi_url=settings.docs_openapi_url if docs_enabled else None,
        docs_url=settings.docs_url if docs_enabled else None,
        redoc_url=settings.docs_redoc_url if docs_enabled else None,
        openapi_prefix=settings.docs_openapi_prefix,
    )

    if settings.prometheus_enabled:
        application.add_middleware(
            PrometheusMiddleware,
            group_paths=settings.prometheus_group_paths,
            app_name=settings.prometheus_app_name,
            prefix=settings.prometheus_prefix,
        )

    application.add_event_handler(
        "startup", start_app_handler(application, settings)
    )
    application.add_event_handler("shutdown", stop_app_handler(application))

    application.include_router(get_router(settings))

    return application


app = get_application()
