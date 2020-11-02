import asyncio

from databases import Database

from {{cookiecutter.project_slug}}.logger import get_logger


log = get_logger("db_checker")


async def check_db_connection(db: Database) -> bool:
    """Check DB connection."""
    msg = "db connection"

    try:
        result = await asyncio.wait_for(
            db.fetch_val("SELECT 1 v;", None, "v"), 0.5
        )
        if result == 1:
            log.info(msg, ok=True)
            return True

    except Exception:
        log.exception(msg, ok=False)
        return False

    log.error(msg, ok=False)
    return False
