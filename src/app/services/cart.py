from uuid import UUID, uuid7
from domain.entities.cart import Cart, CartItem
from infrastructure.repositories.cart.base import BaseCartRepository


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

    async def get_cart_items(self, cart_id: UUID) -> list[CartItem]:
        cart_items = await self._cart_repository.get_cart_items(cart_id=cart_id)
        return cart_items

    async def add_product_to_cart(
        self, cart_id: UUID, product_id: UUID, quantity: int
    ) -> CartItem:
        cart_item = await self._cart_repository.get_cart_item_by_product_id(
            cart_id=cart_id, product_id=product_id
        )

        if cart_item and cart_item.quantity != quantity:
            cart_item.quantity = quantity
            await self._cart_repository.update_cart_item(cart_item)
        elif cart_item is None:
            cart_item = CartItem(
                id=uuid7(),
                cart_id=cart_id,
                product_id=product_id,
            )
            await self._cart_repository.create(cart_item)

        return cart_item

    async def delete_item_in_cart(self, cart_id: UUID, item_id: UUID) -> None:
        await self._cart_repository.delete_item(cart_id=cart_id, item_id=item_id)
