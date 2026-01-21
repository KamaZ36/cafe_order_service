from uuid import UUID

from app.dtos.cart import ResponseCartDTO
from app.services.cart import CartService

from infrastructure.database.transaction_manager.base import TransactionManager


class CreateCartCommand:
    user_id: UUID | None
    session_id: UUID | None


class GetOrCreateCartInteractor:
    def __init__(
        self,
        cart_service: CartService,
        transaction_manager: TransactionManager,
    ) -> None:
        self._cart_service = cart_service
        self._transaction_manager = transaction_manager

    async def __call__(self, data: CreateCartCommand) -> ResponseCartDTO:
        cart = await self._cart_service.get_cart_by_user_id(data.user_id)
        cart_items = await self._cart_service.get_cart_items(cart_id=cart.id)

        cart_dto = ResponseCartDTO(
            id=cart.id,
            items=cart_items,
            created_at=cart.created_at,
            updated_at=cart.updated_at,
        )

        await self._transaction_manager.commit()
        return cart_dto
