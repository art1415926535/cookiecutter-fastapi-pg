import sqlalchemy
from sqlalchemy import Column, Integer, String


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

items = sqlalchemy.Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("title", String, nullable=False),
    Column("description", String),
    Column("price", Integer, nullable=False),
)
