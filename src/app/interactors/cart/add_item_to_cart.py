from dataclasses import dataclass
from uuid import UUID, uuid7

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.product import ProductIsNotAvailable, ProductNotFound
from domain.entities.cart import CartItem
from infrastructure.database.models.cart import CartItemModel
from infrastructure.repositories.cart.base import BaseCartItemRepository
from infrastructure.repositories.product.base import BaseProductRepository


@dataclass(frozen=True, eq=False)
class AddItemToCartQuery:
    user_id: UUID
    product_id: UUID


class AddItemToCartInetractor:
    def __init__(
        self,
        session: AsyncSession,
        product_repository: BaseProductRepository,
        cart_item_repository: BaseCartItemRepository,
    ) -> None:
        self._session = session
        self._product_repository = product_repository
        self._cart_item_repository = cart_item_repository

    async def __call__(self, data: AddItemToCartQuery) -> None:
        product = await self._product_repository.get_by_id(product_id=data.product_id)
        if product is None:
            raise ProductNotFound(product_id=data.product_id)
        if product.is_available is None:
            raise ProductIsNotAvailable(product_name=product.name)

        cart_item = CartItem(
            id=uuid7(),
            user_id=data.user_id,
            product_id=product.id,
        )

        await self._cart_item_repository.create(cart_item)
