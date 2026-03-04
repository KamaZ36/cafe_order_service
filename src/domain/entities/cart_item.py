from dataclasses import dataclass
from uuid import UUID

from domain.entities.mixins import CreatedAtMixin, UpdatedAtMixin


@dataclass(kw_only=True)
class CartItem(CreatedAtMixin, UpdatedAtMixin):
    id: UUID
    product_id: UUID
    quantity: int = 1

    def increase_quantity(self, amount: int = 1) -> None:
        """
        Увеличить количество товара

        :param amount: На сколько увеличить количество
        :type amount: int
        """

        if amount <= 0:
            raise "Значение должно быть положительным."
        self.quantity += amount

    def decrease_quantity(self, amount: int = 1) -> None:
        """
        Уменьшить количество товара

        :param amount: На сколько уменьшить количество
        :type amount: int
        """
        if amount <= 0:
            raise "Значение должно быть положительным."

        new_quantity = self.quantity - amount
        if new_quantity <= 0:
            raise ValueError("Количество будет 0 или отрицательным.")

        self.quantity = new_quantity

    def update_quantity(self, quantity: int) -> None:
        """
        Обновить количество товара

        :param quantity: Количество товара
        :type quantity: int
        """

        if quantity <= 0:
            raise ValueError("Количество не может быть меньше или равно 0")
        self.quantity = quantity

    def __eq__(self, othe_item: "CartItem") -> bool:
        if not isinstance(othe_item, CartItem):
            return False
        return self.product_id == othe_item.product_id
