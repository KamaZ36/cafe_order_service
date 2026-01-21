from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from utils import get_datetime_utc_now


@dataclass
class Cart:
    id: UUID
    user_id: UUID | None
    created_at: datetime
    updated_at: datetime


@dataclass
class CartItem:
    id: UUID
    cart_id: UUID
    product_id: UUID
    quantity: int = 1
    created_at: datetime = field(default_factory=get_datetime_utc_now)
    updated_at: datetime = field(default_factory=get_datetime_utc_now)
