from dataclasses import dataclass
from uuid import UUID


@dataclass
class CartItem:
    id: UUID
    user_id: UUID
    product_id: UUID
    quantity: int = 1
