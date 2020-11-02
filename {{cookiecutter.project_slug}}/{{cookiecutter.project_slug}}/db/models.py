import sqlalchemy
from sqlalchemy import Boolean, Column, Integer, String


convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()]
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": (
        "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s"
    ),
    "pk": "pk__%(table_name)s",
}
metadata = sqlalchemy.MetaData(naming_convention=convention)

users = sqlalchemy.Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("first_name", String),
    Column("last_name", String),
    Column("email", String, unique=True, index=True, nullable=False),
    Column("password", String, nullable=False),
    Column("is_active", Boolean, server_default="true"),
    Column("is_superuser", Boolean, server_default="false"),
)
