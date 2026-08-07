"""add product composition

Revision ID: 64d006302a1b
Revises: ed6d51113663
Create Date: 2026-08-07 00:40:14.733510

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '64d006302a1b'
down_revision: Union[str, Sequence[str], None] = 'ed6d51113663'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('products', sa.Column('composition', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('products', 'composition')
