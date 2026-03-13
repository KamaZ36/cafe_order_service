from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel


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
