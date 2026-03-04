from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.cart import Cart


class BaseCartRepository(ABC):
    @abstractmethod
    async def create(self, cart: Cart) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, cart_id: UUID) -> Cart | None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Cart | None:
        raise NotImplementedError()

    @abstractmethod
    async def save(self, cart: Cart) -> None:
        raise NotImplementedError()
