from dataclasses import dataclass
from uuid import UUID

from zernyshko.app.services.cart import CartService
from zernyshko.domain.exceptions.cart import ProductNotExistInCart
from zernyshko.infrastructure.database.transaction_manager.base import TransactionManager
from zernyshko.infrastructure.identity_provider.base import IdentityProvider
from zernyshko.infrastructure.repositories.cart.base import BaseCartRepository


@dataclass(frozen=True, eq=False)
class UpdateCartItemCommand:
    product_id: UUID
    quantity: int


class UpdateCartItemInteractor:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        cart_service: CartService,
        cart_repository: BaseCartRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self._identity_provider = identity_provider
        self._cart_service = cart_service
        self._cart_repository = cart_repository
        self._transaction_manager = transaction_manager

    async def __call__(self, command: UpdateCartItemCommand) -> None:
        user_id = await self._identity_provider.get_current_user_id_or_none()
        if user_id is None:
            raise ProductNotExistInCart()

        cart = await self._cart_service.get_cart_by_user_id(user_id)

        cart.update_product_quantity(
            product_id=command.product_id, quantity=command.quantity
        )

        await self._cart_repository.save(cart)
        await self._transaction_manager.commit()
