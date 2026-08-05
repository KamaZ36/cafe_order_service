from sqlalchemy import UUID, Column, DateTime, Table, func
from sqlalchemy.dialects.postgresql import INET

from zernyshko.api.auth.model import AuthSession
from zernyshko.infrastructure.database.models.base import mapper_registry

AUTH_SESSION_TABLE = Table(
    "sessions",
    mapper_registry.metadata,
    Column("session_id", UUID, unique=True, primary_key=True),
    Column("user_id", UUID, nullable=True),
    Column("ip_address", INET, nullable=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("expires_at", DateTime(timezone=True), nullable=False),
)

mapper_registry.map_imperatively(AuthSession, AUTH_SESSION_TABLE)
