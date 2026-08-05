"""add user role and password

Revision ID: ef4e87c7bab7
Revises: 3a8ce70755a3
Create Date: 2026-07-19 16:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ef4e87c7bab7"
down_revision: Union[str, Sequence[str], None] = "3a8ce70755a3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    user_role_enum = ENUM("CUSTOMER", "STAFF", name="userrole", create_type=True)
    user_role_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.Enum("CUSTOMER", "STAFF", name="userrole"),
            nullable=False,
            server_default="CUSTOMER",
        ),
    )
    op.add_column("users", sa.Column("password_hash", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "password_hash")
    op.drop_column("users", "role")

    user_role_enum = ENUM("CUSTOMER", "STAFF", name="userrole")
    user_role_enum.drop(op.get_bind(), checkfirst=True)
