from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from domain.entities.cart_item import CartItem


@dataclass(frozen=True, eq=False)
class ResponseCartDTO:
    id: UUID
    total_items: int
    total_price: Decimal
    items: tuple[CartItem]


@dataclass(frozen=True, eq=False)
class ResponseCartItemDTO:
    product_id: UUID
    name: str
    image: str
    price: Decimal
    quantity: int
