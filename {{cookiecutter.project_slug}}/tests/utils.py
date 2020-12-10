from contextlib import contextmanager
from typing import Generator, List, Literal, Union
from urllib.parse import urlsplit
from uuid import UUID

import sqlalchemy_utils


@contextmanager
def temp_db_manager(
    base_db_dsn: str, prefix: str, template=None
) -> Generator[str, None, None]:
    parsed_db_dsn = urlsplit(base_db_dsn)
    parsed_test_db_dsn = parsed_db_dsn._replace(
        path="/" + prefix + parsed_db_dsn.path.lstrip("/")
    )
    test_db_dsn = parsed_test_db_dsn.geturl()

    if sqlalchemy_utils.database_exists(test_db_dsn):
        sqlalchemy_utils.drop_database(test_db_dsn)

    sqlalchemy_utils.create_database(test_db_dsn, template=template)

    try:
        yield test_db_dsn
    finally:
        sqlalchemy_utils.drop_database(test_db_dsn)


def user_payload(
    uuid: Union[str, UUID],
    name: str = "",
    roles: List[Literal["stylist"]] = None,
):
    """Формирование данных для jwt."""
    if roles is None:
        roles = []
    return {
        "sub": str(uuid),
        "name": name,
        "realm_access": {"roles": roles},
        "exp": 2208988800,  # 2040-01-01T00:00:00+00:00
        "aud": "account",
    }
