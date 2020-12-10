import pytest
from databases import Database

from {{cookiecutter.project_slug}} import schemas
from {{cookiecutter.project_slug}} import use_cases as uc
from {{cookiecutter.project_slug}}.db import models


@pytest.mark.asyncio
async def test_get_items(db: Database):
    title = "test_get_items"
    price = 12
    item_id = await db.fetch_val(
        models.items.insert()
        .values(title=title, price=price)
        .returning(models.items.c.id)
    )
    assert isinstance(item_id, int)

    list_items = uc.ListItems(db)
    items = await list_items(1, 0)

    assert len(items) == 1
    assert items[0] == schemas.ItemOut(id=item_id, title=title, price=price)
