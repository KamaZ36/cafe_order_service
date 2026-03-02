from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(kw_only=True)
class Product:
    id: UUID

    name: str
    description: str
    weight: str

    category_id: UUID

    image: str | None = None

    price: Decimal
    is_available: bool = True
    is_popular: bool = False
    is_new: bool = False

    def set_price(self, new_price: Decimal) -> None:
        """Установить новую цену продукта"""

        if new_price < Decimal("0"):
            raise ValueError()

        self.price = new_price

    def set_image(self, image_path: str) -> None:
        """Установить картинку продукта"""

        self.image = image_path
