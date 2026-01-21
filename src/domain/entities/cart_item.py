from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CartItem:
    id: UUID
    user_id: UUID
    product_id: UUID
    quantity: int = 1
    created_at: datetime
    updated_at: datetime
