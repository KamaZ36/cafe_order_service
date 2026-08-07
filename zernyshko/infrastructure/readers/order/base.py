from abc import ABC, abstractmethod
from uuid import UUID

from zernyshko.app.dtos.order import ResponseOrderListDTO
from zernyshko.app.dtos.pagination import Pagination
from zernyshko.domain.entities.order import OrderStatus


class OrderReader(ABC):
    @abstractmethod
    async def get_list_by_user_id(
        self, user_id: UUID, pagination: Pagination
    ) -> ResponseOrderListDTO:
        raise NotImplementedError()

    @abstractmethod
    async def get_list(
        self, pagination: Pagination, status: list[OrderStatus] | None = None
    ) -> ResponseOrderListDTO:
        raise NotImplementedError()
