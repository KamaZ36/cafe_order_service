from sqlalchemy import Table, Column, UUID, func, DateTime
from sqlalchemy.dialects.postgresql import INET

from src.api.auth.model import AuthSession
from src.infrastructure.database.models.base import mapper_registry


AUTH_SESSION_TABLE = Table(
    "sessions",
    mapper_registry.metadata,
    Column("session_id", UUID, unique=True, primary_key=True),
    Column("user_id", UUID, nullable=False),
    Column("ip_address", INET, nullable=True),
    Column("created_at", DateTime, server_default=func.now()),
    Column("expires_at", DateTime, nullable=False),
)

mapper_registry.map_imperatively(AuthSession, AUTH_SESSION_TABLE)
