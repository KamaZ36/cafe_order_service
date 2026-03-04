from dataclasses import dataclass
from uuid import UUID

from domain.entities.cart_item import CartItem


@dataclass(frozen=True, eq=False)
class ResponseCartDTO:
    id: UUID
    items: tuple[CartItem]
