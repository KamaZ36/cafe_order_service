from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, eq=False, kw_only=True)
class ResponseProductDTO:
    name: str

    image: str | None = None

    price: Decimal
    is_available: bool = True
    is_popular: bool = False
    is_new: bool = False
