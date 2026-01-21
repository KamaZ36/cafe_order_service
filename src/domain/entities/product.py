from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass
class Product:
    id: UUID

    name: str
    description: str
    weight: str

    category_id: UUID

    price: Decimal
    is_available: bool = True
    is_popular: bool = False
    is_new: bool = False
