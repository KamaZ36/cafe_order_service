from sqlalchemy import UUID, Column, Enum, String, Table

from zernyshko.domain.entities.user import User, UserRole
from zernyshko.infrastructure.database.models.base import mapper_registry

USER_TABLE = Table(
    "users",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True, unique=True),
    Column("phone_number", String, unique=False, nullable=True),
    Column(
        "role", Enum(UserRole), nullable=False, server_default=UserRole.CUSTOMER.value
    ),
    Column("password_hash", String, nullable=True),
)


mapper_registry.map_imperatively(
    User,
    USER_TABLE,
    properties={
        "_id": USER_TABLE.c.id,
        "_phone_number": USER_TABLE.c.phone_number,
        "_role": USER_TABLE.c.role,
        "_password_hash": USER_TABLE.c.password_hash,
    },
)
