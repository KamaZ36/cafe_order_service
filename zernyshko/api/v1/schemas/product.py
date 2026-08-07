from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProductResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str
    weight: str
    composition: str | None
    category_id: UUID
    image: str | None
    price: Decimal
    is_available: bool
    is_popular: bool
    is_new: bool


class CreateProductSchema(BaseModel):
    user_id: UUID
    name: str
    description: str
    weight: str
    category_id: UUID
    price: Decimal
    is_available: bool = True
    is_popular: bool = False
    is_new: bool = False


class GetProductListSchema(BaseModel):
    limit: int
    offset: int
    search: str | None = None
    category_id: UUID | None = None
