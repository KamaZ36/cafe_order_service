from datetime import datetime

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid7

from domain.entities.order import Order, OrderType
from domain.entities.order_item import OrderItem

from app.interactors.common import AuthenticatedCommand
from app.services.cart import CartService

from infrastructure.database.transaction_manager.base import TransactionManager
from infrastructure.repositories.order.base import OrderRepository
from infrastructure.repositories.product.base import ProductRepository


@dataclass(frozen=True, eq=False)
class CreateOrderCommand(AuthenticatedCommand):
    desired_time: datetime
    comment: str | None = None


class CreateOrderInteractor:
    def __init__(
        self,
        cart_service: CartService,
        product_repository: ProductRepository,
        order_repository: OrderRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self._cart_service = cart_service
        self._product_repository = product_repository
        self._order_repository = order_repository
        self._transaction_manager = transaction_manager

    async def __call__(self, command: CreateOrderCommand) -> UUID:
        cart = await self._cart_service.get_cart_by_user_id(command.user_id)

        if cart.total_items == 0:
            raise ValueError()

        order_id = uuid7()
        order_number = await self.generate_order_number()
        order_items = []
        total_price = Decimal(0)

        products = await self._product_repository.get_by_ids(cart.items.keys())

        for cart_item in cart.get_items:
            product = products[cart_item.product_id]
            item_total_price = product.price * cart_item.quantity
            total_price += item_total_price

            order_item = OrderItem(
                id=uuid7(),
                order_id=order_id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price_at_order=product.price,
                item_total_price=item_total_price,
            )
            order_items.append(order_item)

        order = Order(
            id=order_id,
            order_number=order_number,
            user_id=command.user_id,
            items=order_items,
            order_type=OrderType.PICKUP,
            desired_time=self.remove_tz(command.desired_time),
            total_amount=total_price,
            comment=command.comment,
        )

        await self._order_repository.create(order)
        await self._cart_service.delete_cart(cart)

        await self._transaction_manager.commit()

        return order.id

    async def generate_order_number(self) -> str:
        return "123"

    def remove_tz(self, date: datetime) -> datetime:
        if date.tzinfo is not None:
            date = date.replace(tzinfo=None)

        return date
