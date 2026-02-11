from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.domain.entities.cart_item import CartItem


@dataclass(frozen=True, eq=False)
class ResponseCartDTO:
    id: UUID
    items: tuple[CartItem]
