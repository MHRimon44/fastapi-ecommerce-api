"""add role to users

Revision ID: f0f382fcc171
Revises: e978b0dce145
Create Date: auto-generated

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f0f382fcc171"
down_revision: Union[str, Sequence[str], None] = "e978b0dce145"
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


def upgrade() -> None:
    if _table_exists("users") and not _column_exists("users", "role"):
        op.add_column(
            "users",
            sa.Column(
                "role",
                sa.String(length=30),
                nullable=False,
                server_default="Customer",
            ),
        )


def downgrade() -> None:
    if _table_exists("users") and _column_exists("users", "role"):
        op.drop_column("users", "role")
