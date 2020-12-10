from pathlib import Path
from subprocess import PIPE, STDOUT, Popen
from typing import Optional

import click
import uvicorn

from {{cookiecutter.project_slug}} import logger
from {{cookiecutter.project_slug}}.db.alembic import migration_manager
from {{cookiecutter.project_slug}}.db.wait_for_db import sync_wait_for_db
from {{cookiecutter.project_slug}}.logger import LOG_LEVEL
from {{cookiecutter.project_slug}}.settings import ServiceSettings


log = logger.get_logger()
module = "{{cookiecutter.project_slug}}"
app = f"{module}.server:app"
alembic_path = str(Path(module, "db", "alembic"))


@click.group(help=f"{module} cli")
@click.pass_context
def cli(ctx):
    """Group of commands."""
    ctx.ensure_object(dict)

    service_settings = ServiceSettings()
    ctx.obj["service_settings"] = service_settings


@cli.command()
@click.option("--host", "-h", default="0.0.0.0", help="host")
@click.option("--port", "-p", default={{cookiecutter.default_port}}, help="port")
@click.option("--reload", "-r", is_flag=True, help="enable auto-reload")
@click.pass_context
def serve(ctx, host: str, port: int, reload: bool):
    """Serve application by uvicorn."""
    log.info("Click: serve", host=host, port=port, reload=reload)

    service_settings: ServiceSettings = ctx.obj["service_settings"]

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_config=None,
        log_level=LOG_LEVEL,
        access_log=service_settings.uvicorn_access_log,
        debug=service_settings.fastapi_debug,
        reload=reload,
    )


@cli.command()
@click.option("--message", "-m", help="revision message")
@click.option("--dsn", help="db url")
@click.pass_context
def makemigrations(ctx, message: Optional[str], dsn: Optional[str]):
    """Creates new migrations."""
    log.info("Click: makemigrations", message=message)
    if not message:
        message = input("Message: ")

    if dsn is None:
        service_settings: ServiceSettings = ctx.obj["service_settings"]
        dsn = service_settings.pg_dsn

    migration_manager.revision(alembic_path, dsn, message)


@cli.command()
@click.argument(
    "action", default="upgrade", type=click.Choice(["upgrade", "downgrade"])
)
@click.option("--dsn", help="db url")
@click.option("--revision", "-r", help="revision number", default="head")
@click.option(
    "--sql",
    is_flag=True,
    help="only generating sql scripts (a.k.a. “offline mode”)",
)
@click.pass_context
def migrate(ctx, action: str, dsn: Optional[str], revision: str, sql: bool):
    """Apply migrations."""
    log.info("Click: migrate", action=action)

    if dsn is None:
        service_settings: ServiceSettings = ctx.obj["service_settings"]
        dsn = service_settings.pg_dsn

    cmd = {
        "upgrade": migration_manager.upgrade,
        "downgrade": migration_manager.downgrade,
    }
    cmd[action](alembic_path, dsn, revision, sql)


def _log_subprocess_output(tool, pipe):
    for line in iter(pipe.readline, b""):  # b'\n'-separated lines
        log.info(line.decode().replace("\n", "\t"), tool=tool)


@cli.command()
def fmt():
    """Format python files."""
    log.info("Click: fmt")

    cmds = [
        ["isort", "."],
        ["black", "."],
    ]
    for cmd in cmds:
        tool = cmd[0]
        log.info(f"▶️ Start {tool}")
        process = Popen(cmd, stdout=PIPE, stderr=STDOUT)
        with process.stdout:
            _log_subprocess_output(tool, process.stdout)
        process.wait()


@cli.command()
def lint():
    """Run linters."""
    log.info("Click: lint")

    cmds = [
        ["flake8", module, "tests"],
        ["mypy", module, "tests"],
        ["isort", "--check-only", "."],
        ["black", "--check", "."],
    ]

    for cmd in cmds:
        tool = cmd[0]
        log.info(f"▶️ Start {tool}")
        process = Popen(cmd, stdout=PIPE, stderr=STDOUT)
        with process.stdout:
            _log_subprocess_output(tool, process.stdout)

        exit_code = process.wait()
        if exit_code:
            log.critical(tool, exit_code=exit_code)
            exit(exit_code)


@cli.command()
@click.option("--wait-for-db", help="wait db")
def test(wait_for_db: Optional[str] = None):
    """Run tests."""
    import pytest

    if wait_for_db:
        sync_wait_for_db(wait_for_db, tries=15, delay=2)
    exit(pytest.main(["tests"]))


if __name__ == "__main__":
    cli(obj={})
