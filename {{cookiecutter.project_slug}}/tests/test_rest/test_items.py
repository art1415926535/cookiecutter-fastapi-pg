from typing import Callable
from uuid import uuid4

import httpx
import pytest
from databases import Database

from tests.utils import user_payload
from {{cookiecutter.project_slug}}.db import models


@pytest.mark.asyncio
async def test_items(
    client_builder: Callable[..., httpx.AsyncClient], db: Database
):
    item_id = await db.fetch_val(
        models.items.insert()
        .values(title="title", price=10)
        .returning(models.items.c.id)
    )
    assert isinstance(item_id, int)

    user_uuid = uuid4()
    async with client_builder(jwt_payload=user_payload(uuid=user_uuid)) as c:
        response = await c.get("/items")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": item_id,
            "title": "title",
            "description": None,
            "price": 10,
        }
    ]


@pytest.mark.asyncio
async def test_auth(client: httpx.AsyncClient, db: Database):
    response = await client.get("/items")

    assert response.status_code == 401
