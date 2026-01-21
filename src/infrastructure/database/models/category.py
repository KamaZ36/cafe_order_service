from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from models.base import BaseModel


class CategoryModel(BaseModel):
    __tablename__ = "categories"

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
