from sqlalchemy import UUID, Column, String, Table

from zernyshko.domain.entities.category import Category
from zernyshko.infrastructure.database.models.base import mapper_registry

CATEGORY_TABLE = Table(
    "categories",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True, unique=True),
    Column("name", String, nullable=False, unique=True),
)

mapper_registry.map_imperatively(
    Category,
    CATEGORY_TABLE,
    properties={
        "_id": CATEGORY_TABLE.c.id,
        "_name": CATEGORY_TABLE.c.name,
    },
)
