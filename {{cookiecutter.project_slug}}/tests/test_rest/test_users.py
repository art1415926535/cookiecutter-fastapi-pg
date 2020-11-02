import pytest
from databases import Database
from httpx import AsyncClient

from {{cookiecutter.project_slug}}.db import models


@pytest.mark.asyncio
async def test_users(client: AsyncClient, db: Database):
    user_id = await db.fetch_val(
        models.users.insert()
        .values(email="a@a.aa", password="1")
        .returning(models.users.c.id)
    )
    assert isinstance(user_id, int)
    response = await client.get("/users")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": user_id,
            "first_name": None,
            "last_name": None,
            "is_active": True,
            "is_superuser": False,
            "email": "a@a.aa",
        }
    ]
