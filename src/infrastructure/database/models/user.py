from sqlalchemy import Column, Table, UUID, String

from domain.entities.user import User
from infrastructure.database.models.base import mapper_registry


USER_TABLE = Table(
    "users",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True, unique=True),
    Column("phone_number", String, unique=True),
)


mapper_registry.map_imperatively(User, USER_TABLE)
