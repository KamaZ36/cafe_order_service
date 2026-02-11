from sqlalchemy import Table, Column, UUID, String

from src.domain.entities.category import Category
from src.infrastructure.database.models.base import mapper_registry


CATEGORY_TABLE = Table(
    "categories",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True, unique=True),
    Column("name", String, nullable=False, unique=True),
)

mapper_registry.map_imperatively(Category, CATEGORY_TABLE)
