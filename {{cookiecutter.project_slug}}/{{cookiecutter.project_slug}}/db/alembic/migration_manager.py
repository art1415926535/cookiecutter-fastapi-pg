from alembic import command
from alembic.config import Config

from {{cookiecutter.project_slug}}.logger import get_logger


log = get_logger()


def revision(script_location: str, dsn: str, message: str) -> None:
    alembic_cfg = _config_init(script_location, dsn)
    log.info("▶️ Running revision generation", script_location=script_location)
    command.revision(alembic_cfg, autogenerate=True, message=message)


def upgrade(script_path: str, dsn: str, revision: str, sql: bool) -> None:
    alembic_cfg = _config_init(script_path, dsn)
    log.info("▶️ Running upgrade migrations", script_location=script_path)
    command.upgrade(alembic_cfg, revision, sql)


def downgrade(script_path: str, dsn: str, revision: str, sql: bool) -> None:
    alembic_cfg = _config_init(script_path, dsn)
    log.info("▶️ Running downgrade migrations", script_location=script_path)
    command.downgrade(alembic_cfg, revision, sql)


def _config_init(script_path: str, dsn: str) -> Config:
    log.info("Alembic config initialization", script_location=script_path)

    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", script_path)
    alembic_cfg.set_main_option("sqlalchemy.url", dsn)
    filename_format = (
        "%%(year)d_%%(month).2d_%%(day).2d_"
        "%%(hour).2d%%(minute).2d%%(second).2d_%%(slug)s"
    )
    alembic_cfg.set_main_option("file_template", filename_format)

    alembic_cfg.set_section_option("post_write_hooks", "hooks", "black isort")
    alembic_cfg.set_section_option(
        "post_write_hooks", "black.type", "console_scripts"
    )
    alembic_cfg.set_section_option(
        "post_write_hooks", "black.entrypoint", "black"
    )
    alembic_cfg.set_section_option(
        "post_write_hooks", "isort.type", "console_scripts"
    )
    alembic_cfg.set_section_option(
        "post_write_hooks", "isort.entrypoint", "isort"
    )
    return alembic_cfg
