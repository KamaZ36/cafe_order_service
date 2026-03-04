from dataclasses import dataclass, field
from uuid import UUID, uuid7

from domain.entities.cart_item import CartItem
from domain.entities.mixins import CreatedAtMixin, UpdatedAtMixin


@dataclass(kw_only=True)
class Cart(CreatedAtMixin, UpdatedAtMixin):
    id: UUID
    user_id: UUID | None
    items: dict[UUID, CartItem] = field(default_factory=dict)

    @property
    def get_items(self) -> tuple[CartItem]:
        """Получить список элементов корзины"""
        return tuple(self.items.values())

    @property
    def total_items(self) -> int:
        """Получить количество товаров в корзине"""
        return sum(item.quantity for item in self.items.values())

    def add_item(self, product_id: UUID, quantity: int = 1) -> None:
        """
        Добавить товар в корзину

        :param product_id: ID продукта
        :type product_id: UUID
        :param price: Цена продукта
        :type price: Decimal
        :param quantity: Количество позиций продукта
        :type quantity: int
        """

        if quantity <= 0:
            raise ValueError("Количество товаров не может быть 0")

        if product_id in self.items:
            item = self.items[product_id]
            item.increase_quantity(amount=quantity)
        else:
            item = CartItem(id=uuid7(), product_id=product_id, quantity=quantity)
            self.items[product_id] = item

    def update_item_quantity(self, product_id: UUID, quantity: int) -> None:
        """
        Docstring for update_item_quantity

        :param product_id: ID товара в корзине
        :type product_id: UUID
        :param quantity: Новое количество товара в корзине
        :type quantity: int
        """

        if product_id not in self.items:
            raise ValueError("Продукт не найден в корзине")

        item = self.items[product_id]

        if quantity == 0:
            self.remove_item(product_id=product_id)
        else:
            item.update_quantity(quantity=quantity)

    def remove_item(self, product_id: UUID) -> None:
        """
        Удалить товар из корзины

        :param product_id: ID продукта в корзине
        :type product_id: UUID
        """

        if product_id not in self.items:
            raise ValueError("Продукт не найден в корзине")
        del self.items[product_id]
