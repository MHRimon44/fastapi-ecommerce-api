"""add role to users

Revision ID: f0f382fcc171
Revises: e978b0dce145
Create Date: 2026-06-28 05:36:50.925159

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0f382fcc171'
down_revision: Union[str, Sequence[str], None] = 'e978b0dce145'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
