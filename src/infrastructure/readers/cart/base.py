from abc import ABC, abstractmethod
from uuid import UUID

from app.dtos.cart import ResponseCartDTO


class BaseCartReader(ABC):
    @abstractmethod
    async def get_by_id(self, cart_id: UUID) -> ResponseCartDTO | None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> ResponseCartDTO | None:
        raise NotImplementedError()
