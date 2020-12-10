from typing import Final, List, Optional

import sentry_sdk
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.exceptions import HTTPException
from starlette_exporter import PrometheusMiddleware

from {{cookiecutter.project_slug}}.core import app_event_handler, request_context
from {{cookiecutter.project_slug}}.rest import exception_handlers
from {{cookiecutter.project_slug}}.rest.deps import update_oauth2_scheme
from {{cookiecutter.project_slug}}.rest.router import get_router
from {{cookiecutter.project_slug}}.settings import ServiceSettings


OPENAPI_TAGS: Final[List[dict]] = []


def get_application(settings: Optional[ServiceSettings] = None):
    """Application factory."""

    if settings is None:
        settings = ServiceSettings()

    docs_enabled = settings.docs_enabled
    application = FastAPI(
        title=settings.app_title,
        version=settings.app_version,
        openapi_tags=OPENAPI_TAGS,
        debug=settings.fastapi_debug,
        openapi_url=settings.docs_openapi_url if docs_enabled else None,
        docs_url=settings.docs_url if docs_enabled else None,
        redoc_url=settings.docs_redoc_url if docs_enabled else None,
        openapi_prefix=settings.docs_openapi_prefix,
        root_path=settings.fastapi_root_path,
    )

    if settings.prometheus_enabled:
        application.add_middleware(
            PrometheusMiddleware,
            group_paths=settings.prometheus_group_paths,
            app_name=settings.prometheus_app_name,
            prefix=settings.prometheus_prefix,
        )

    if settings.keycloak_url is not None:
        keycloak_url = settings.keycloak_url
        realm = settings.keycloak_realm
        update_oauth2_scheme(
            f"{keycloak_url}auth/realms/{realm}/protocol/openid-connect/auth",
            f"{keycloak_url}auth/realms/{realm}/protocol/openid-connect/token",
        )

    application.add_event_handler(
        "startup", app_event_handler.start_app_handler(application, settings)
    )
    application.add_event_handler(
        "shutdown", app_event_handler.stop_app_handler(application)
    )

    application.include_router(get_router(settings))
    application.middleware("http")(request_context.add_log_context)
    application.exception_handler(HTTPException)(
        exception_handlers.http_exception_handler
    )
    application.exception_handler(RequestValidationError)(
        exception_handlers.validation_exception_handler
    )

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        sample_rate=settings.sentry_traces_sample_rate,
        release=settings.app_version,
    )

    return application


app = SentryAsgiMiddleware(get_application())
