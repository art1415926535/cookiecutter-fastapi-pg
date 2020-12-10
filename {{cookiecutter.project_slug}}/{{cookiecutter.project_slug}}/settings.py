from typing import Optional

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn

from . import SERVICE_NAME, __author__, __version__


class ServiceSettings(BaseSettings):
    """Service settings."""

    app_title: str = SERVICE_NAME
    app_version: str = __version__

    # Uvicorn
    uvicorn_access_log: bool = False

    # FastAPI
    fastapi_debug: bool = False
    fastapi_admin_route_prefix: str = "admin"
    fastapi_root_path: str = ""

    # Docs
    docs_enabled: bool = False
    docs_url: str = "/docs"
    docs_openapi_prefix: str = ""
    docs_openapi_url: str = "/openapi.json"
    docs_redoc_url: str = "/redoc"
    docs_admin_route_include_in_schema: bool = False

    # PostgreSQL
    pg_dsn: PostgresDsn  # e.g.: 'postgres://user:pass@localhost:5432/foobar'
    pg_pool_min_size: int = 5
    pg_pool_max_size: int = 20
    pg_application_name: str = SERVICE_NAME
    pg_command_timeout: Optional[float] = None

    # JWT
    jwt_secret: str = ""
    jwt_algorithm: str = "RS256"
    jwt_audience: Optional[str] = None

    # Keycloak
    keycloak_url: Optional[str]
    keycloak_realm: Optional[str]

    # Prometheus
    prometheus_enabled: bool = True
    prometheus_group_paths: bool = True
    prometheus_app_name: str = SERVICE_NAME
    prometheus_prefix: str = __author__

    # Sentry
    sentry_dsn: Optional[AnyHttpUrl] = None
    sentry_traces_sample_rate: float = 1.0

    class Config:
        env_file = ".env"
        validate_assignment = True
