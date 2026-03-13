from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True, eq=False, kw_only=True)
class ResponseProductDTO:
    name: str
    description: str
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

    is_available: bool
    is_popular: bool
    is_new: bool


@dataclass(frozen=True, eq=False, kw_only=True)
class ResponseProductListDTO:
    total_count: int
    count: int
    products: list[ResponseProductForListDTO]
