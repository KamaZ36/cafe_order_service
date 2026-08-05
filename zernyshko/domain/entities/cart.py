from datetime import datetime
from uuid import UUID, uuid7

from zernyshko.domain.entities.cart_item import CartItem
from zernyshko.domain.entities.mixins import CreatedAtMixin, UpdatedAtMixin
from zernyshko.domain.exceptions.cart import ProductNotExistInCart


class Cart(CreatedAtMixin, UpdatedAtMixin):
    def __init__(
        self,
        id: UUID,
        user_id: UUID | None,
        items: dict[UUID, CartItem] | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        CreatedAtMixin.__init__(self, created_at)
        UpdatedAtMixin.__init__(self, updated_at)
        self._id = id
        self._user_id = user_id
        self._items = items if items is not None else {}

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def user_id(self) -> UUID | None:
        return self._user_id

    @property
    def items(self) -> dict[UUID, CartItem]:
        return self._items

    @property
    def get_items(self) -> tuple[CartItem, ...]:
        return tuple(self._items.values())

    @property
    def total_items(self) -> int:
        return sum(item.quantity for item in self._items.values())

    def check_product_exist(self, product_id: UUID) -> bool:
        return product_id in self._items if self._items else False

    def add_item(self, product_id: UUID, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("Количество товаров не может быть 0")

        if product_id in self._items:
            item = self._items[product_id]
            item.increase_quantity(amount=quantity)
        else:
            item = CartItem(id=uuid7(), product_id=product_id, quantity=quantity)
            self._items[product_id] = item

    def update_product_quantity(self, product_id: UUID, quantity: int) -> None:
        if product_id not in self._items:
            raise ProductNotExistInCart()

        item = self._items[product_id]

        if quantity == 0:
            self.remove_item(product_id=product_id)
        else:
            item.update_quantity(quantity=quantity)

    def remove_item(self, product_id: UUID) -> None:
        if product_id not in self._items:
            return

        del self._items[product_id]

    def clear(self) -> None:
        self._items.clear()
