from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from infrastructure.database.models.base import BaseModel


class CartItemModel(BaseModel):
    __tablename__ = "cart_items"

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(default=1)
