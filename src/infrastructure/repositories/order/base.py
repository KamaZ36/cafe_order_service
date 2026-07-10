from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.order import Order


class OrderRepository(ABC):
    @abstractmethod
    async def create(self, order: Order) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Order | None:
        raise NotImplementedError()
