from sqlalchemy import Table, Column, UUID, String, DECIMAL, Boolean, ForeignKey

from src.domain.entities.product import Product
from src.infrastructure.database.models.base import mapper_registry


PRODUCT_TABLE = Table(
    "products",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True, unique=True),
    Column("name", String(100), nullable=False),
    Column("description", String, nullable=False),
    Column("weight", String, nullable=True),
    Column("category_id", UUID, ForeignKey("categories.id")),
    Column("price", DECIMAL(precision=10, scale=2), nullable=False),
    Column("is_available", Boolean, server_default="True"),
    Column("is_popular", Boolean, server_default="False"),
    Column("is_new", Boolean, server_default="False"),
)

mapper_registry.map_imperatively(Product, PRODUCT_TABLE)
