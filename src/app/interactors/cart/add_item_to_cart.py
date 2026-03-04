from dataclasses import dataclass
from uuid import UUID

from app.exceptions.product import (
    IncorretQuantityValue,
    ProductIsNotAvailable,
    ProductNotFound,
)
from app.services.cart import CartService
from app.interactors.common import AuthenticatedCommand

from infrastructure.database.transaction_manager.base import TransactionManager
from infrastructure.repositories.cart.base import BaseCartRepository
from infrastructure.repositories.product.base import BaseProductRepository


@dataclass(frozen=True, eq=False)
class AddItemToCartCommand(AuthenticatedCommand):
    product_id: UUID
    quantity: int


class AddItemToCartInetractor:
    def __init__(
        self,
        transaction_manager: TransactionManager,
        product_repository: BaseProductRepository,
        cart_service: CartService,
        cart_repository: BaseCartRepository,
    ) -> None:
        self._transaction_manager = transaction_manager
        self._product_repository = product_repository
        self._cart_repository = cart_repository
        self._cart_service = cart_service

    async def __call__(self, command: AddItemToCartCommand) -> None:
        if command.quantity >= 5:
            raise IncorretQuantityValue()

        cart = await self._cart_service.get_cart_by_user_id(command.user_id)

        product = await self._product_repository.get_by_id(
            product_id=command.product_id
        )
        if product is None:
            raise ProductNotFound(product_id=command.product_id)
        if not product.is_available:
            raise ProductIsNotAvailable(product_name=product.name)

        cart.add_item(product_id=command.product_id, quantity=command.quantity)

        await self._cart_repository.save(cart)
        await self._transaction_manager.commit()
