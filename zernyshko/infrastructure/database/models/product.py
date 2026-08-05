from sqlalchemy import DECIMAL, UUID, Boolean, Column, ForeignKey, String, Table

from zernyshko.domain.entities.product import Product
from zernyshko.infrastructure.database.models.base import mapper_registry

PRODUCT_TABLE = Table(
    "products",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True, unique=True),
    Column("name", String(100), nullable=False),
    Column("description", String, nullable=False),
    Column("weight", String, nullable=True),
    Column("category_id", UUID, ForeignKey("categories.id")),
    Column("price", DECIMAL(precision=10, scale=2), nullable=False),
    Column("image", String, nullable=True, server_default=None),
    Column("is_available", Boolean, server_default="True"),
    Column("is_popular", Boolean, server_default="False"),
    Column("is_new", Boolean, server_default="False"),
)

mapper_registry.map_imperatively(
    Product,
    PRODUCT_TABLE,
    properties={
        "_id": PRODUCT_TABLE.c.id,
        "_name": PRODUCT_TABLE.c.name,
        "_description": PRODUCT_TABLE.c.description,
        "_weight": PRODUCT_TABLE.c.weight,
        "_category_id": PRODUCT_TABLE.c.category_id,
        "_price": PRODUCT_TABLE.c.price,
        "_image": PRODUCT_TABLE.c.image,
        "_is_available": PRODUCT_TABLE.c.is_available,
        "_is_popular": PRODUCT_TABLE.c.is_popular,
        "_is_new": PRODUCT_TABLE.c.is_new,
    },
)
