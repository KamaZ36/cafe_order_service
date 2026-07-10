from dataclasses import dataclass, field
import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from domain.entities.order_item import OrderItem


class OrderType(str, Enum):
    PICKUP = "PICKUP"
    DELIVERY = "DELIVERY"


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    READY = "READY"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


@dataclass(kw_only=True)
class Order:
    id: UUID
    order_number: str
    user_id: UUID

    items: list[OrderItem] = field(default_factory=list)

    order_type: OrderType
    status: OrderStatus = OrderStatus.PENDING

    desired_time: datetime

    total_amount: Decimal

    delivery_address: str | None = None
    delivery_entrance: str | None = None
    delivery_floor: int | None = None
    delivery_intercom: str | None = None

    comment: str | None = None
