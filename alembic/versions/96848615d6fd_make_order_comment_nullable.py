"""make order comment nullable

Revision ID: 96848615d6fd
Revises: 1591edf3cd22
Create Date: 2026-08-03 13:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "96848615d6fd"
down_revision: Union[str, Sequence[str], None] = "1591edf3cd22"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("orders", "comment", existing_type=sa.String(), nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("UPDATE orders SET comment = '' WHERE comment IS NULL")
    op.alter_column("orders", "comment", existing_type=sa.String(), nullable=False)
