from decimal import Decimal
from uuid import UUID


class Product:
    def __init__(
        self,
        id: UUID,
        name: str,
        description: str,
        weight: str,
        category_id: UUID,
        price: Decimal,
        image: str | None = None,
        is_available: bool = True,
        is_popular: bool = False,
        is_new: bool = False,
        composition: str | None = None,
    ) -> None:
        self._id = id
        self._name = name
        self._description = description
        self._weight = weight
        self._composition = composition
        self._category_id = category_id
        self._image = image
        self._price = price
        self._is_available = is_available
        self._is_popular = is_popular
        self._is_new = is_new

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def weight(self) -> str:
        return self._weight

    @property
    def composition(self) -> str | None:
        return self._composition

    @property
    def category_id(self) -> UUID:
        return self._category_id

    @property
    def image(self) -> str | None:
        return self._image

    @property
    def price(self) -> Decimal:
        return self._price

    @property
    def is_available(self) -> bool:
        return self._is_available

    @property
    def is_popular(self) -> bool:
        return self._is_popular

    @property
    def is_new(self) -> bool:
        return self._is_new

    def set_price(self, new_price: Decimal) -> None:
        if new_price < Decimal("0"):
            raise ValueError()
        self._price = new_price

    def set_image(self, image_path: str) -> None:
        self._image = image_path

    def set_name(self, name: str) -> None:
        self._name = name

    def set_description(self, description: str) -> None:
        self._description = description

    def set_weight(self, weight: str) -> None:
        self._weight = weight

    def set_composition(self, composition: str | None) -> None:
        self._composition = composition

    def set_category_id(self, category_id: UUID) -> None:
        self._category_id = category_id

    def set_availability(self, is_available: bool) -> None:
        self._is_available = is_available

    def set_popular(self, is_popular: bool) -> None:
        self._is_popular = is_popular

    def set_new(self, is_new: bool) -> None:
        self._is_new = is_new
