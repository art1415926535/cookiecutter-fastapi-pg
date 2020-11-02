import pytest
from databases import Database

from {{cookiecutter.project_slug}}.db import connection
from {{cookiecutter.project_slug}}.settings import ServiceSettings


@pytest.mark.asyncio
async def test_connection(service_settings: ServiceSettings):
    db: Database = await connection.connect_to_db(service_settings)

    v = await db.fetch_val("select 1;")
    assert v == 1

    await connection.close_db_connection(db)
    assert not db.is_connected
