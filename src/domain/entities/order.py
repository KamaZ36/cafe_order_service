from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(kw_only=True)
class Order:
    id: UUID
    order_number: str
    user_id: UUID
    cart_id: UUID

    total_amount: Decimal
    comment: str | None = None
