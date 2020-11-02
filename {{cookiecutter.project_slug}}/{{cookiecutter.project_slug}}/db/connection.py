from typing import Optional, Protocol

from databases import Database
from pydantic import PostgresDsn

from {{cookiecutter.project_slug}}.logger import get_logger


log = get_logger("db_events")


class _PostgreSQLSettings(Protocol):
    pg_dsn: PostgresDsn
    pg_pool_min_size: int = 5
    pg_pool_max_size: int = 20
    pg_application_name: str
    pg_command_timeout: Optional[float]


async def connect_to_db(settings: _PostgreSQLSettings) -> Database:
    """Create Database connection."""
    log.error(
        "connecting",
        scheme=settings.pg_dsn.scheme,
        host=settings.pg_dsn.host,
        port=settings.pg_dsn.port,
        path=settings.pg_dsn.path,
    )

    db = Database(
        settings.pg_dsn,
        min_size=settings.pg_pool_min_size,
        max_size=settings.pg_pool_max_size,
        command_timeout=settings.pg_command_timeout,
        server_settings={"application_name": settings.pg_application_name},
    )
    await db.connect()
    log.error("connection established")
    return db


async def close_db_connection(db: Database) -> None:
    """Close Database connection."""
    log.error("closing connection to database")

    await db.disconnect()

    log.error("connection closed")
