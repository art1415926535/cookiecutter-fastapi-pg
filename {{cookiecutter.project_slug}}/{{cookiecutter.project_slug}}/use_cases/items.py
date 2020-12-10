from typing import List

import sqlalchemy

from {{cookiecutter.project_slug}} import schemas
from {{cookiecutter.project_slug}}.db import models
from {{cookiecutter.project_slug}}.logger import get_logger

from .base import DatabaseUseCase
from .errors import Error


log = get_logger()


class ListItems(DatabaseUseCase):
    async def __call__(self, limit: int, offset: int) -> List[schemas.ItemOut]:
        query = (
            sqlalchemy.select(
                [
                    models.items.c.id,
                    models.items.c.title,
                    models.items.c.description,
                    models.items.c.price,
                ]
            )
            .limit(limit)
            .offset(offset)
        )
        log.debug("items select", query=str(query))
        try:
            db_items: list = await self.db.fetch_all(query)
        except Exception:
            raise Error(msg="fetch from db error", user_msg="Oops...")
        log.info("items selected from db", count=len(db_items))

        items = [schemas.ItemOut.parse_obj(u) for u in db_items]
        return items
