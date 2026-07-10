from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.order import Order
from infrastructure.repositories.order.base import OrderRepository


class SQLAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, order: Order) -> None:
        self._session.add(order)

    async def get_by_id(self, order_id: UUID) -> Order | None:
        order = await self._session.get(Order, order_id)
        return order if order else None
