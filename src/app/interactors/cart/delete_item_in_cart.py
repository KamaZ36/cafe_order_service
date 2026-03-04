from dataclasses import dataclass
from uuid import UUID

from app.interactors.common import AuthenticatedCommand
from app.services.cart import CartService

from infrastructure.database.transaction_manager.base import TransactionManager
from infrastructure.repositories.cart.base import BaseCartRepository


@dataclass(frozen=True, eq=False)
class DeleteItemInCartCommand(AuthenticatedCommand):
    product_id: UUID


class DeleteItemInCart:
    def __init__(
        self,
        cart_service: CartService,
        cart_repository: BaseCartRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self._cart_service = cart_service
        self._cart_repository = cart_repository
        self._transaction_manager = transaction_manager

    async def __call__(self, command: DeleteItemInCartCommand) -> None:
        cart = await self._cart_service.get_cart_by_user_id(command.user_id)

        cart.remove_item(command.product_id)

        await self._cart_repository.save(cart)
        await self._transaction_manager.commit()
