from typing import Callable

from fastapi import FastAPI

from {{cookiecutter.project_slug}}.db.connection import (
    close_db_connection,
    connect_to_db,
)
from {{cookiecutter.project_slug}}.settings import ServiceSettings


def start_app_handler(app: FastAPI, settings: ServiceSettings) -> Callable:
    """Create start_app function."""

    async def start_app() -> None:
        app.state.db = await connect_to_db(settings)

    return start_app


def stop_app_handler(app: FastAPI) -> Callable:
    """Create stop_app function."""

    async def stop_app() -> None:
        await close_db_connection(app.state.db)

    return stop_app
