"""store timestamps with timezone

Revision ID: 1591edf3cd22
Revises: ef4e87c7bab7
Create Date: 2026-08-03 12:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1591edf3cd22"
down_revision: Union[str, Sequence[str], None] = "ef4e87c7bab7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TIMESTAMP_COLUMNS = [
    ("sessions", "created_at"),
    ("sessions", "expires_at"),
    ("carts", "created_at"),
    ("carts", "updated_at"),
    ("cart_items", "created_at"),
    ("cart_items", "updated_at"),
    ("orders", "desired_time"),
]


def upgrade() -> None:
    """Upgrade schema."""
    for table, column in TIMESTAMP_COLUMNS:
        op.alter_column(
            table,
            column,
            type_=sa.DateTime(timezone=True),
            postgresql_using=f"{column} AT TIME ZONE 'UTC'",
        )


def downgrade() -> None:
    """Downgrade schema."""
    for table, column in TIMESTAMP_COLUMNS:
        op.alter_column(
            table,
            column,
            type_=sa.DateTime(timezone=False),
            postgresql_using=f"{column} AT TIME ZONE 'UTC'",
        )
