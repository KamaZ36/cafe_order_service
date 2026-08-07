from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from zernyshko.domain.entities.order import OrderStatus, OrderType


@dataclass(frozen=True, eq=False, kw_only=True)
class ResponseOrderItemDTO:
    product_id: UUID
    name: str
    price_at_order: Decimal
    item_total_price: Decimal
    quantity: int


@dataclass(frozen=True, eq=False, kw_only=True)
class ResponseOrderForListDTO:
    id: UUID
    order_number: str
    status: OrderStatus
    order_type: OrderType
    desired_time: datetime
    total_amount: Decimal
    comment: str | None
    created_at: datetime
    items: tuple[ResponseOrderItemDTO, ...]
    customer_phone_number: str | None
    cancel_reason: str | None


@dataclass(frozen=True, eq=False, kw_only=True)
class ResponseOrderListDTO:
    total_count: int
    count: int
    orders: list[ResponseOrderForListDTO]


@dataclass(frozen=True, eq=False, kw_only=True)
class CreateOrderResultDTO:
    order_id: UUID
    payment_confirmation_url: str
