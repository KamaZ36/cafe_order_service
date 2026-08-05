from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, Table, func
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_keyed_dict

from zernyshko.domain.entities.cart import Cart
from zernyshko.domain.entities.cart_item import CartItem
from zernyshko.infrastructure.database.models.base import mapper_registry

CART_TABLE = Table(
    "carts",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True, unique=True),
    Column("user_id", UUID, ForeignKey("users.id")),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    ),
)

CART_ITEM_TABLE = Table(
    "cart_items",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True, unique=True),
    Column("cart_id", UUID, ForeignKey("carts.id")),
    Column("product_id", UUID, ForeignKey("products.id")),
    Column("quantity", Integer, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    ),
)


mapper_registry.map_imperatively(
    Cart,
    CART_TABLE,
    properties={
        "_id": CART_TABLE.c.id,
        "_user_id": CART_TABLE.c.user_id,
        "_created_at": CART_TABLE.c.created_at,
        "_updated_at": CART_TABLE.c.updated_at,
        "_items": relationship(
            CartItem,
            cascade="all, delete-orphan",
            collection_class=attribute_keyed_dict("product_id"),
        ),
    },
)
mapper_registry.map_imperatively(
    CartItem,
    CART_ITEM_TABLE,
    properties={
        "_id": CART_ITEM_TABLE.c.id,
        "_product_id": CART_ITEM_TABLE.c.product_id,
        "_quantity": CART_ITEM_TABLE.c.quantity,
        "_created_at": CART_ITEM_TABLE.c.created_at,
        "_updated_at": CART_ITEM_TABLE.c.updated_at,
    },
)
