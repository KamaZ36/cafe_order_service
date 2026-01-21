from uuid import UUID
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from models.base import BaseModel


class ProductModel(BaseModel):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str]
    weight: Mapped[str] = mapped_column(nullable=False)

    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )

    price: Mapped[Decimal] = mapped_column(nullable=False)
    is_available: Mapped[bool] = mapped_column(default=True)
    is_popular: Mapped[bool] = mapped_column(default=False)
    is_new: Mapped[bool] = mapped_column(default=False)
