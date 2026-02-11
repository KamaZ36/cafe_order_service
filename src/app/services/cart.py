from uuid import UUID, uuid7

from src.domain.entities.cart import Cart
from src.domain.entities.cart_item import CartItem

from src.infrastructure.repositories.cart.base import BaseCartRepository


class CartService:
    def __init__(self, cart_repository: BaseCartRepository) -> None:
        self._cart_repository = cart_repository

    async def create_cart(self, user_id: UUID) -> Cart:
        cart = Cart(id=uuid7(), user_id=user_id)
        await self._cart_repository.create(cart)
        return cart

    async def get_cart_by_user_id(self, user_id: UUID) -> Cart:
        cart = await self._cart_repository.get_by_user_id(user_id)
        if cart is None:
            cart = await self.create_cart(user_id=user_id)
        return cart
