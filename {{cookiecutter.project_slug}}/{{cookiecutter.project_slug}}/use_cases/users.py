from typing import Final

import asyncpg
import sqlalchemy

from {{cookiecutter.project_slug}} import schemas
from {{cookiecutter.project_slug}}.core import security
from {{cookiecutter.project_slug}}.db import models
from {{cookiecutter.project_slug}}.logger import get_logger

from .base import DatabaseUseCase
from .errors import UseCaseError


log = get_logger()


class ListUsers(DatabaseUseCase):
    async def __call__(self, limit: int, offset: int) -> schemas.Users:
        query = (
            sqlalchemy.select(
                [
                    models.users.c.id,
                    models.users.c.first_name,
                    models.users.c.last_name,
                    models.users.c.email,
                    models.users.c.is_active,
                    models.users.c.is_superuser,
                ]
            )
            .limit(limit)
            .offset(offset)
        )
        log.debug("users select", query=str(query))

        db_users: list = await self.db.fetch_all(query)
        log.info("users selected from db", count=len(db_users))

        users = [schemas.User.parse_obj(u) for u in db_users]
        return users


class CreateUser(DatabaseUseCase):
    EMAIL_DUPLICATE_ERR: Final[
        str
    ] = 'duplicate key value violates unique constraint "ix__users__email"'

    async def __call__(self, user_create: schemas.UserCreate) -> schemas.User:
        query = await self._build_query(user_create)

        try:
            user_id: int = await self.db.execute(query)
        except asyncpg.exceptions.UniqueViolationError as e:
            if str(e).startswith(self.EMAIL_DUPLICATE_ERR):
                raise UseCaseError(
                    "This email address is already used",
                    loc=["email"],
                    email=user_create.email,
                ) from e
            raise

        self._log_created_user(user_id, user_create)

        user = schemas.User(id=user_id, **user_create.dict())
        return user

    @staticmethod
    async def _build_query(user_create: schemas.UserCreate):
        query = (
            models.users.insert()
            .values(
                first_name=user_create.first_name,
                last_name=user_create.last_name,
                email=user_create.email,
                password=security.get_password_hash(user_create.password),
                is_active=user_create.is_active,
                is_superuser=user_create.is_superuser,
            )
            .returning(models.users.c.id)
        )
        log.debug("user insert", query=str(query))
        return query

    @staticmethod
    def _log_created_user(user_id: int, user_create: schemas.UserCreate):
        user_info = user_create.dict()
        user_info["password"] = "***"
        log.info("user insert executed", user_id=user_id, **user_info)
