from sqlalchemy import (
    DECIMAL,
    UUID,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    func,
)
from sqlalchemy.orm import relationship

from zernyshko.domain.entities.order import Order, OrderStatus, OrderType
from zernyshko.domain.entities.order_item import OrderItem
from zernyshko.infrastructure.database.models.base import mapper_registry

ORDER_TABLE = Table(
    "orders",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True, unique=True),
    Column("order_number", String, nullable=False),
    Column("user_id", UUID, ForeignKey("users.id")),
    Column("order_type", Enum(OrderType), nullable=False),
    Column("status", Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING),
    Column("desired_time", DateTime(timezone=True), nullable=False),
    Column("total_amount", DECIMAL(10, 2), nullable=False),
    Column("delivery_address", String),
    Column("delivery_entrance", String),
    Column("delivery_floor", Integer),
    Column("delivery_intercom", String),
    Column("comment", String, nullable=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("cancel_reason", String, nullable=True),
)


ORDER_ITEM_TABLE = Table(
    "order_items",
    mapper_registry.metadata,
    Column("id", UUID, primary_key=True, unique=True),
    Column("order_id", UUID, ForeignKey("orders.id")),
    Column("product_id", UUID, ForeignKey("products.id")),
    Column("quantity", Integer, nullable=False, server_default="1"),
    Column("price_at_order", DECIMAL(precision=10, scale=2), nullable=False),
    Column("item_total_price", DECIMAL(precision=10, scale=2), nullable=False),
)


mapper_registry.map_imperatively(
    Order,
    ORDER_TABLE,
    properties={
        "_id": ORDER_TABLE.c.id,
        "_order_number": ORDER_TABLE.c.order_number,
        "_user_id": ORDER_TABLE.c.user_id,
        "_order_type": ORDER_TABLE.c.order_type,
        "_status": ORDER_TABLE.c.status,
        "_desired_time": ORDER_TABLE.c.desired_time,
        "_total_amount": ORDER_TABLE.c.total_amount,
        "_delivery_address": ORDER_TABLE.c.delivery_address,
        "_delivery_entrance": ORDER_TABLE.c.delivery_entrance,
        "_delivery_floor": ORDER_TABLE.c.delivery_floor,
        "_delivery_intercom": ORDER_TABLE.c.delivery_intercom,
        "_comment": ORDER_TABLE.c.comment,
        "_created_at": ORDER_TABLE.c.created_at,
        "_cancel_reason": ORDER_TABLE.c.cancel_reason,
        "_items": relationship(OrderItem),
    },
)
mapper_registry.map_imperatively(
    OrderItem,
    ORDER_ITEM_TABLE,
    properties={
        "_id": ORDER_ITEM_TABLE.c.id,
        "_order_id": ORDER_ITEM_TABLE.c.order_id,
        "_product_id": ORDER_ITEM_TABLE.c.product_id,
        "_quantity": ORDER_ITEM_TABLE.c.quantity,
        "_price_at_order": ORDER_ITEM_TABLE.c.price_at_order,
        "_item_total_price": ORDER_ITEM_TABLE.c.item_total_price,
    },
)
