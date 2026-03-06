from pydantic import BaseModel


class UpdateCartItemSchema(BaseModel):
    quantity: int
