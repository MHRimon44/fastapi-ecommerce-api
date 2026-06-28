"""add product active status

Revision ID: 2618fd41bfc6
Revises: '888fc322af6e'
Create Date: auto-generated

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "2618fd41bfc6"
down_revision: Union[str, Sequence[str], None] = '888fc322af6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(table_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return table_name in inspector.get_table_names()


def _column_exists(table_name: str, column_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if table_name not in inspector.get_table_names():
        return False

    columns = inspector.get_columns(table_name)
    return column_name in [column["name"] for column in columns]


def _index_exists(table_name: str, index_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if table_name not in inspector.get_table_names():
        return False

    indexes = inspector.get_indexes(table_name)
    return index_name in [index["name"] for index in indexes]


def upgrade() -> None:
    if _table_exists("products") and not _column_exists("products", "is_active"):
        op.add_column(
            "products",
            sa.Column(
                "is_active",
                sa.Boolean(),
                nullable=False,
                server_default=sa.true(),
            ),
        )

    if _table_exists("products") and not _index_exists("products", "ix_products_is_active"):
        op.create_index(
            "ix_products_is_active",
            "products",
            ["is_active"],
            unique=False,
        )


def downgrade() -> None:
    if _table_exists("products"):
        if _index_exists("products", "ix_products_is_active"):
            op.drop_index("ix_products_is_active", table_name="products")

        if _column_exists("products", "is_active"):
            op.drop_column("products", "is_active")
