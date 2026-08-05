from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True, eq=False, kw_only=True)
class ResponseProductDTO:
    id: UUID
    name: str
    description: str
    weight: str
    category_id: UUID
    price: Decimal

    image: str | None

    is_available: bool
    is_popular: bool
    is_new: bool


@dataclass(frozen=True, eq=False, kw_only=True)
class ResponseProductForListDTO:
    id: UUID
    name: str
    image: str
    price: Decimal
    category_id: UUID

    is_available: bool
    is_popular: bool
    is_new: bool


@dataclass(frozen=True, eq=False, kw_only=True)
class ResponseProductListDTO:
    total_count: int
    count: int
    products: list[ResponseProductForListDTO]
