from uuid import UUID
from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    phone_number: str


class AddItemToCartSchema(BaseModel):
    product_id: UUID
    quantity: int = 1
