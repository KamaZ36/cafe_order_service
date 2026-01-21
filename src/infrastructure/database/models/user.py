from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column

from models.base import BaseModel


class Base(BaseModel):
    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)
