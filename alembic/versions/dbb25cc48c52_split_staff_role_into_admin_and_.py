"""split staff role into admin and barista

Revision ID: dbb25cc48c52
Revises: 795e8bf682dd
Create Date: 2026-08-05 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dbb25cc48c52"
down_revision: Union[str, Sequence[str], None] = "795e8bf682dd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Существующий персонал (роль STAFF) становится полноправным ADMIN —
    # это единственная роль персонала до этой миграции.
    op.execute("ALTER TYPE userrole RENAME VALUE 'STAFF' TO 'ADMIN'")
    op.execute("ALTER TYPE userrole ADD VALUE 'BARISTA'")


def downgrade() -> None:
    """Downgrade schema."""
    # Postgres не поддерживает удаление значения enum напрямую — пересобираем
    # тип. Упадёт, если в таблице уже есть строки с ролью BARISTA.
    op.execute("ALTER TYPE userrole RENAME TO userrole_old")
    op.execute("CREATE TYPE userrole AS ENUM ('CUSTOMER', 'STAFF')")
    op.execute(
        "ALTER TABLE users ALTER COLUMN role TYPE userrole "
        "USING (CASE role::text WHEN 'ADMIN' THEN 'STAFF' ELSE role::text END)::userrole"
    )
    op.execute("DROP TYPE userrole_old")
