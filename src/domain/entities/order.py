from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


class Order:
    id: UUID
    order_number: str
    user_id: UUID
    cart_id: UUID

    total_amount: Decimal
    comment: str | None = None
