from sqlalchemy import Table, Column, UUID, DECIMAL, String, Integer, ForeignKey

from src.domain.entities.order import Order
from src.domain.entities.order_item import OrderItem
from src.infrastructure.database.models.base import mapper_registry


ORDER_TABLE = Table(
    "orders",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True, unique=True),
    Column("order_number", String, nullable=False),
    Column("user_id", UUID, ForeignKey("users.id")),
    Column("cart_id", UUID, ForeignKey("carts.id")),
    Column("total_amount", DECIMAL(precision=10, scale=2), nullable=False),
    Column("comment", String, nullable=False),
)


ORDER_ITEM_TABLE = Table(
    "order_items",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True, unique=True),
    Column("order_id", UUID, ForeignKey("orders.id")),
    Column("product_id", UUID, ForeignKey("products.id")),
    Column("quantity", Integer, nullable=False, server_default="1"),
    Column("price_at_order", DECIMAL(precision=10, scale=2), nullable=False),
    Column("subtotal", DECIMAL(precision=10, scale=2), nullable=False),
)


mapper_registry.map_imperatively(Order, ORDER_TABLE)
mapper_registry.map_imperatively(OrderItem, ORDER_ITEM_TABLE)
