from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.entities.cart import CartItem


@dataclass(frozen=True, eq=False)
class ResponseCartDTO:
    id: UUID
    items: list[CartItem]
    created_at: datetime
    updated_at: datetime
