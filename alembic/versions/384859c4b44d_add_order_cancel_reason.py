"""add order cancel reason

Revision ID: 384859c4b44d
Revises: 6c8b25dcfb62
Create Date: 2026-08-06 12:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "384859c4b44d"
down_revision: Union[str, Sequence[str], None] = "6c8b25dcfb62"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("orders", sa.Column("cancel_reason", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("orders", "cancel_reason")
