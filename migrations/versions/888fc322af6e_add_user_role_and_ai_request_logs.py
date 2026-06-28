"""add user role and ai request logs

Revision ID: 888fc322af6e
Revises: f0f382fcc171
Create Date: 2026-06-28 06:42:00.871988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "888fc322af6e"
down_revision: Union[str, Sequence[str], None] = "f0f382fcc171"
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
    bind = op.get_bind()
    dialect_name = bind.dialect.name

    if _table_exists("users"):
        if not _column_exists("users", "role"):
            op.add_column(
                "users",
                sa.Column(
                    "role",
                    sa.String(length=30),
                    nullable=False,
                    server_default="Customer",
                ),
            )

        op.execute("UPDATE users SET role = 'Customer' WHERE role IS NULL")

        if dialect_name != "sqlite":
            op.alter_column(
                "users",
                "role",
                existing_type=sa.String(length=30),
                nullable=False,
                server_default="Customer",
            )

        if not _index_exists("users", "ix_users_role"):
            op.create_index(
                "ix_users_role",
                "users",
                ["role"],
                unique=False,
            )

    if not _table_exists("ai_request_logs"):
        op.create_table(
            "ai_request_logs",
            sa.Column("log_id", sa.Integer(), nullable=False),
            sa.Column("module_name", sa.String(length=100), nullable=False),
            sa.Column("endpoint", sa.String(length=200), nullable=False),
            sa.Column("status_code", sa.Integer(), nullable=False),
            sa.Column("user_identifier", sa.String(length=150), nullable=True),
            sa.Column("request_body", sa.Text(), nullable=False),
            sa.Column("response_body", sa.Text(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint("log_id"),
        )

    if _table_exists("ai_request_logs"):
        if not _index_exists("ai_request_logs", "ix_ai_request_logs_module_name"):
            op.create_index(
                "ix_ai_request_logs_module_name",
                "ai_request_logs",
                ["module_name"],
                unique=False,
            )

        if not _index_exists("ai_request_logs", "ix_ai_request_logs_endpoint"):
            op.create_index(
                "ix_ai_request_logs_endpoint",
                "ai_request_logs",
                ["endpoint"],
                unique=False,
            )

        if not _index_exists("ai_request_logs", "ix_ai_request_logs_status_code"):
            op.create_index(
                "ix_ai_request_logs_status_code",
                "ai_request_logs",
                ["status_code"],
                unique=False,
            )

        if not _index_exists("ai_request_logs", "ix_ai_request_logs_user_identifier"):
            op.create_index(
                "ix_ai_request_logs_user_identifier",
                "ai_request_logs",
                ["user_identifier"],
                unique=False,
            )

        if not _index_exists("ai_request_logs", "ix_ai_request_logs_created_at"):
            op.create_index(
                "ix_ai_request_logs_created_at",
                "ai_request_logs",
                ["created_at"],
                unique=False,
            )


def downgrade() -> None:
    if _table_exists("ai_request_logs"):
        if _index_exists("ai_request_logs", "ix_ai_request_logs_created_at"):
            op.drop_index("ix_ai_request_logs_created_at", table_name="ai_request_logs")

        if _index_exists("ai_request_logs", "ix_ai_request_logs_user_identifier"):
            op.drop_index("ix_ai_request_logs_user_identifier", table_name="ai_request_logs")

        if _index_exists("ai_request_logs", "ix_ai_request_logs_status_code"):
            op.drop_index("ix_ai_request_logs_status_code", table_name="ai_request_logs")

        if _index_exists("ai_request_logs", "ix_ai_request_logs_endpoint"):
            op.drop_index("ix_ai_request_logs_endpoint", table_name="ai_request_logs")

        if _index_exists("ai_request_logs", "ix_ai_request_logs_module_name"):
            op.drop_index("ix_ai_request_logs_module_name", table_name="ai_request_logs")

        op.drop_table("ai_request_logs")

    if _table_exists("users"):
        if _index_exists("users", "ix_users_role"):
            op.drop_index("ix_users_role", table_name="users")

        if _column_exists("users", "role"):
            op.drop_column("users", "role")
