from uuid import UUID

from app.exceptions.product import ProductIsNotInCart
from infrastructure.repositories.cart.base import BaseCartItemRepository


class DeleteItemInCart:
    def __init__(self, cart_item_repository: BaseCartItemRepository) -> None:
        self._cart_item_repository = cart_item_repository

    async def __call__(self, cart_item_id: UUID) -> None:
        cart_item = await self._cart_item_repository.get_by_id(cart_item_id)
        if cart_item is None:
            raise ProductIsNotInCart()

        await self._cart_item_repository.delete(cart_item_id)
