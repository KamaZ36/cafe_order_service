"""order created_at and order_number sequence

Revision ID: 795e8bf682dd
Revises: 96848615d6fd
Create Date: 2026-08-05 10:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "795e8bf682dd"
down_revision: Union[str, Sequence[str], None] = "96848615d6fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "orders",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.execute("CREATE SEQUENCE order_number_seq START WITH 1000")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP SEQUENCE order_number_seq")
    op.drop_column("orders", "created_at")
