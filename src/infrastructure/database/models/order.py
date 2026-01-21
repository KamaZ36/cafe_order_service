from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from models.base import BaseModel


class OrderModel(BaseModel):
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)
    order_number: Mapped[str] = mapped_column(nullable=False, unique=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    cart_id: Mapped[UUID] = mapped_column(ForeignKey("carts.id"), nullable=False)

    total_amount: Mapped[Decimal] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(nullable=True)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItemModel(BaseModel):
    __tablename__ = "order_items"

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)
    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(default=1, nullable=False)
    price_at_order: Mapped[Decimal] = mapped_column(nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
