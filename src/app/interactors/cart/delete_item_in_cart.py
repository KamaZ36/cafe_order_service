from dataclasses import dataclass
from uuid import UUID

from app.services.cart import CartService


@dataclass(frozen=True, eq=False)
class DeleteItemInCartCommand:
    user_id: UUID
    cart_id: UUID
    item_id: UUID


class DeleteItemInCart:
    def __init__(self, cart_service: CartService) -> None:
        self._cart_service = cart_service

    async def __call__(self, data: DeleteItemInCartCommand) -> None:
        await self._cart_service.delete_item_in_cart(
            cart_id=data.cart_id, item_id=data.cart_id
        )
