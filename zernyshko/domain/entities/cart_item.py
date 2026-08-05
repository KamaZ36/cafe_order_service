from datetime import datetime
from uuid import UUID

from zernyshko.domain.entities.mixins import CreatedAtMixin, UpdatedAtMixin


class CartItem(CreatedAtMixin, UpdatedAtMixin):
    def __init__(
        self,
        id: UUID,
        product_id: UUID,
        quantity: int = 1,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        CreatedAtMixin.__init__(self, created_at)
        UpdatedAtMixin.__init__(self, updated_at)
        self._id = id
        self._product_id = product_id
        self._quantity = quantity

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def product_id(self) -> UUID:
        return self._product_id

    @property
    def quantity(self) -> int:
        return self._quantity

    def increase_quantity(self, amount: int = 1) -> None:
        if amount <= 0:
            raise ValueError("Значение должно быть положительным.")
        self._quantity += amount

    def decrease_quantity(self, amount: int = 1) -> None:
        if amount <= 0:
            raise ValueError("Значение должно быть положительным.")

        new_quantity = self._quantity - amount
        if new_quantity <= 0:
            raise ValueError("Количество будет 0 или отрицательным.")

        self._quantity = new_quantity

    def update_quantity(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Количество не может быть меньше или равно 0")
        self._quantity = quantity

    def __eq__(self, other_item: "CartItem") -> bool:
        if not isinstance(other_item, CartItem):
            return False
        return self._product_id == other_item._product_id
