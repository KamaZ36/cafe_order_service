"""add awaiting_payment order status

Revision ID: ed6d51113663
Revises: 31c4ca4bb26a
Create Date: 2026-08-06 22:28:47.398642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed6d51113663'
down_revision: Union[str, Sequence[str], None] = '31c4ca4bb26a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE orderstatus ADD VALUE 'AWAITING_PAYMENT' BEFORE 'PENDING'")


def downgrade() -> None:
    """Downgrade schema."""
    # PostgreSQL не поддерживает удаление значения из enum-типа.
    pass
