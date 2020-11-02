from typing import Callable, Type

from databases import Database
from fastapi import Depends, Request

from {{cookiecutter.project_slug}}.use_cases import DatabaseUseCase


def db(request: Request) -> Database:
    return request.app.state.db


def use_case(
    repository_type: Type[DatabaseUseCase],
) -> Callable[[], DatabaseUseCase]:
    def wrap(db_: Database = Depends(db)) -> DatabaseUseCase:
        return repository_type(db_)

    return wrap
