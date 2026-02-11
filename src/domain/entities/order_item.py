from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(kw_only=True)
class OrderItem:
    id: UUID
    order_id: UUID
    product_id: UUID
    quantity: int = 1
    price_at_order: Decimal
    subtotal: Decimal
