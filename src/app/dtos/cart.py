from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from domain.entities.cart_item import CartItem


@dataclass(eq=False)
class ResponseCartDTO:
    id: UUID
    total_items: int
    total_price: Decimal
    items: tuple[ResponseCartItemDTO]


@dataclass(eq=False)
class ResponseCartItemDTO:
    product_id: UUID
    name: str
    image: str
    price: Decimal
    item_total_price: Decimal
    quantity: int
