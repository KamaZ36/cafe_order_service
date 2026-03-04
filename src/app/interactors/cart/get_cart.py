from dataclasses import dataclass

from app.dtos.cart import ResponseCartDTO
from app.services.cart import CartService
from app.interactors.common import AuthenticatedCommand

from infrastructure.database.transaction_manager.base import TransactionManager


@dataclass(frozen=True, eq=False)
class GetCartQuery(AuthenticatedCommand):
    pass


class GetOrCreateCartInteractor:
    def __init__(
        self,
        cart_service: CartService,
        transaction_manager: TransactionManager,
    ) -> None:
        self._cart_service = cart_service
        self._transaction_manager = transaction_manager

    async def __call__(self, data: GetCartQuery) -> ResponseCartDTO:
        cart = await self._cart_service.get_cart_by_user_id(data.user_id)

        cart_dto = ResponseCartDTO(id=cart.id, items=cart.get_items)

        await self._transaction_manager.commit()
        return cart_dto
