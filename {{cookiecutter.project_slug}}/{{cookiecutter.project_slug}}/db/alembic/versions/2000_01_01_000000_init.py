"""
init

Revision ID: 000000000000
Revises:
Create Date: 2000-01-01 00:00:00.000000
"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "000000000000"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "is_active", sa.Boolean(), server_default="true", nullable=True
        ),
        sa.Column(
            "is_superuser", sa.Boolean(), server_default="false", nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__users")),
    )
    op.create_index(op.f("ix__users__email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix__users__id"), "users", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix__users__id"), table_name="users")
    op.drop_index(op.f("ix__users__email"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###