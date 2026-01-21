from dataclasses import dataclass
from uuid import UUID, uuid7

from app.exceptions.product import (
    IncorretQuantityValue,
    ProductIsNotAvailable,
    ProductNotFound,
)

from app.services.cart import CartService
from domain.entities.cart import CartItem

from infrastructure.database.transaction_manager.base import TransactionManager
from infrastructure.repositories.cart.base import BaseCartRepository
from infrastructure.repositories.product.base import BaseProductRepository


@dataclass(frozen=True, eq=False)
class AddItemToCartCommand:
    user_id: UUID
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

    async def __call__(self, data: AddItemToCartCommand) -> CartItem:
        if data.quantity >= 5:
            raise IncorretQuantityValue()

        cart = await self._cart_service.get_cart_by_user_id(data.user_id)

        product = await self._product_repository.get_by_id(product_id=data.product_id)
        if product is None:
            raise ProductNotFound(product_id=data.product_id)
        if not product.is_available:
            raise ProductIsNotAvailable(product_name=product.name)

        cart_item = await self._cart_service.add_product_to_cart(
            cart_id=cart.id, product_id=data.product_id, quantity=data.quantity
        )

        await self._transaction_manager.commit()
        return cart_item
