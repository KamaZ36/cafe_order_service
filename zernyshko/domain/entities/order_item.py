from decimal import Decimal
from uuid import UUID


class OrderItem:
    def __init__(
        self,
        id: UUID,
        order_id: UUID,
        product_id: UUID,
        price_at_order: Decimal,
        item_total_price: Decimal,
        quantity: int = 1,
    ) -> None:
        self._id = id
        self._order_id = order_id
        self._product_id = product_id
        self._quantity = quantity
        self._price_at_order = price_at_order
        self._item_total_price = item_total_price

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def order_id(self) -> UUID:
        return self._order_id

    @property
    def product_id(self) -> UUID:
        return self._product_id

    @property
    def quantity(self) -> int:
        return self._quantity

    @property
    def price_at_order(self) -> Decimal:
        return self._price_at_order

    @property
    def item_total_price(self) -> Decimal:
        return self._item_total_price
