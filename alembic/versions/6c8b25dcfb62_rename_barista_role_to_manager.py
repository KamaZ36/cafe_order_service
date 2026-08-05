"""rename barista role to manager

Revision ID: 6c8b25dcfb62
Revises: dbb25cc48c52
Create Date: 2026-08-06 10:00:00.000000

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6c8b25dcfb62"
down_revision: Union[str, Sequence[str], None] = "dbb25cc48c52"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # BARISTA переосмыслена как MANAGER: теперь это роль про меню и заказы
    # кафе, а не буквально "бариста"
    op.execute("ALTER TYPE userrole RENAME VALUE 'BARISTA' TO 'MANAGER'")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TYPE userrole RENAME VALUE 'MANAGER' TO 'BARISTA'")
