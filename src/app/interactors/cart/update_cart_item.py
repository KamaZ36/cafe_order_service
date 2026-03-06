from dataclasses import dataclass
from uuid import UUID

from app.services.cart import CartService
from app.interactors.common import AuthenticatedCommand

from infrastructure.database.transaction_manager.base import TransactionManager
from infrastructure.repositories.cart.base import BaseCartRepository


@dataclass(frozen=True, eq=False)
class UpdateCartItemCommand(AuthenticatedCommand):
    product_id: UUID
    quantity: int


class UpdateCartItemInteractor:
    def __init__(
        self,
        cart_service: CartService,
        cart_repository: BaseCartRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self._cart_service = cart_service
        self._cart_repository = cart_repository
        self._transaction_manager = transaction_manager

    async def __call__(self, command: UpdateCartItemCommand) -> None:
        cart = await self._cart_service.get_cart_by_user_id(command.user_id)

        cart.update_product_quantity(
            product_id=command.product_id, quantity=command.quantity
        )

        await self._cart_repository.save(cart)
        await self._transaction_manager.commit()
