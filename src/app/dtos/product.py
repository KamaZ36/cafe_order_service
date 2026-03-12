from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, eq=False, kw_only=True)
class ResponseProductDTO:
    name: str
    description: str
    price: Decimal

    image: str | None = None

    is_available: bool = True
    is_popular: bool = False
    is_new: bool = False


@dataclass(frozen=True, eq=False, kw_only=True)
class ResponseProductForListDTO:
    name: str
    image: str
    price: Decimal

    is_available: bool = True
    is_popular: bool = False
    is_new: bool = False
    
@dataclass(frozen=True, eq=False, kw_only=True)
class ResponseProductListDTO:
    total: int 
    
