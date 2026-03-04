from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.cart import Cart

from infrastructure.repositories.cart.base import BaseCartRepository


class SQLAlchemyCartRepository(BaseCartRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, cart: Cart):
        self._session.add(cart)

    async def get_by_id(self, cart_id: UUID) -> Cart | None:
        cart = await self._session.get(Cart, cart_id)
        return cart if cart else None

    async def get_by_user_id(self, user_id: UUID) -> Cart | None:
        query = (
            select(Cart)
            .where(Cart.user_id == user_id)
            .options(selectinload(Cart.items))
        )
        result = await self._session.execute(query)
        cart = result.scalar_one_or_none()
        return cart

    async def save(self, cart: Cart) -> None:
        pass
