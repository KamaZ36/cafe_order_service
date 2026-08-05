from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid7

from zernyshko.app.exceptions.user import UserNotFound, UserPhoneNumberRequired
from zernyshko.app.services.cart import CartService
from zernyshko.domain.entities.order import Order, OrderType
from zernyshko.domain.entities.order_item import OrderItem
from zernyshko.infrastructure.database.transaction_manager.base import TransactionManager
from zernyshko.infrastructure.identity_provider.base import IdentityProvider
from zernyshko.infrastructure.repositories.order.base import OrderRepository
from zernyshko.infrastructure.repositories.product.base import ProductRepository
from zernyshko.infrastructure.repositories.user.base import BaseUserRepository


@dataclass(frozen=True, eq=False)
class CreateOrderCommand:
    desired_time: datetime
    comment: str | None = None


class CreateOrderInteractor:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        cart_service: CartService,
        product_repository: ProductRepository,
        order_repository: OrderRepository,
        user_repository: BaseUserRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self._identity_provider = identity_provider
        self._cart_service = cart_service
        self._product_repository = product_repository
        self._order_repository = order_repository
        self._user_repository = user_repository
        self._transaction_manager = transaction_manager

    async def __call__(self, command: CreateOrderCommand) -> UUID:
        user_id = await self._identity_provider.get_current_user_id()

        user = await self._user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id=user_id)
        if not user.phone_number:
            raise UserPhoneNumberRequired()

        cart = await self._cart_service.get_cart_by_user_id(user_id)

        if cart.total_items == 0:
            raise ValueError()

        order_id = uuid7()
        order_number = await self._order_repository.get_next_order_number()
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
            user_id=user_id,
            items=order_items,
            order_type=OrderType.PICKUP,
            desired_time=self.ensure_utc(command.desired_time),
            total_amount=total_price,
            comment=command.comment,
        )

        await self._order_repository.create(order)
        await self._cart_service.delete_cart(cart)

        await self._transaction_manager.commit()

        return order.id

    def ensure_utc(self, date: datetime) -> datetime:
        if date.tzinfo is None:
            return date.replace(tzinfo=timezone.utc)

        return date.astimezone(timezone.utc)
