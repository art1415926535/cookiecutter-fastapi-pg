from pathlib import Path
from typing import AsyncGenerator, Callable, Generator
from urllib.parse import urlparse

import asgi_lifespan
import fastapi
import httpx
import jose.jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from databases import Database

from {{cookiecutter.project_slug}}.db import connection
from {{cookiecutter.project_slug}}.db.alembic import migration_manager
from {{cookiecutter.project_slug}}.server import get_application
from {{cookiecutter.project_slug}}.settings import ServiceSettings

from . import utils


module = "{{cookiecutter.project_slug}}"
alembic_path = str(Path(module, "db", "alembic"))


@pytest.fixture(scope="session")
def private_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=512)


@pytest.fixture(scope="session")
def private_key_str(private_key) -> str:
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()


@pytest.fixture(scope="session")
def base_service_settings(private_key) -> ServiceSettings:
    settings = ServiceSettings()

    public_key = (
        private_key.public_key()
        .public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        .decode()
    )
    settings.jwt_secret = public_key
    settings.jwt_algorithm = "RS256"
    settings.jwt_audience = "account"

    return settings


@pytest.fixture(scope="session")
def default_pg_dsn(base_service_settings: ServiceSettings) -> str:
    return base_service_settings.pg_dsn


@pytest.fixture(scope="session")
def migrated_postgres_template(
    default_pg_dsn: str,
) -> Generator[str, None, None]:
    """
    Creates temporary database and applies migrations.
    Database can be used as template to fast creation databases for tests.
    Has "session" scope, so is called only once per tests run.
    """
    with utils.temp_db_manager(default_pg_dsn, "template_") as test_db_dsn:
        migration_manager.upgrade(alembic_path, test_db_dsn, "head", False)
        yield test_db_dsn


@pytest.fixture
def test_db_dsn(
    default_pg_dsn: str, migrated_postgres_template: str
) -> Generator[str, None, None]:
    """
    Quickly creates clean migrated database using temporary database as base.
    Use this fixture in tests that require migrated database.
    """
    template_db = urlparse(migrated_postgres_template).path.lstrip("/")

    with utils.temp_db_manager(
        default_pg_dsn, "test_", template=template_db
    ) as db_dsn:
        yield db_dsn


@pytest.fixture
def service_settings(
    base_service_settings: ServiceSettings, test_db_dsn: str
) -> ServiceSettings:
    settings = base_service_settings.copy(deep=True)
    settings.pg_dsn = test_db_dsn  # type: ignore
    return settings


@pytest.fixture
@pytest.mark.asyncio
async def db(
    service_settings: ServiceSettings, test_db_dsn: str
) -> AsyncGenerator[Database, None]:
    db: Database = await connection.connect_to_db(service_settings)
    yield db
    await connection.close_db_connection(db)


@pytest.fixture
@pytest.mark.asyncio
async def app(
    service_settings: ServiceSettings,
) -> AsyncGenerator[fastapi.FastAPI, None]:
    application = get_application(settings=service_settings)
    async with asgi_lifespan.LifespanManager(application):
        yield application


@pytest.fixture
def client_builder(
    app: fastapi.FastAPI,
    private_key_str: str,
    service_settings: ServiceSettings,
) -> Callable[..., httpx.AsyncClient]:
    def builder(jwt_payload=None, **kwargs) -> httpx.AsyncClient:
        if jwt_payload:
            jwt = jose.jwt.encode(
                jwt_payload,
                private_key_str,
                algorithm=service_settings.jwt_algorithm,
            )
            kwargs.setdefault("headers", {})
            kwargs["headers"].update({"Authorization": f"Bearer {jwt}"})

        client = httpx.AsyncClient(app=app, base_url="http://test", **kwargs)
        return client

    return builder


@pytest.fixture
@pytest.mark.asyncio
async def client(client_builder: Callable[..., httpx.AsyncClient]):
    async with client_builder() as c:
        yield c
