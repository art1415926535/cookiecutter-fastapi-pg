from contextlib import contextmanager
from typing import Generator
from urllib.parse import urlsplit

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

    sqlalchemy_utils.create_database(test_db_dsn, template=template)

    try:
        yield test_db_dsn
    finally:
        sqlalchemy_utils.drop_database(test_db_dsn)
