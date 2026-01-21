from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.cart import CartItem


class BaseCartItemRepository(ABC):
    @abstractmethod
    async def create(self, cart_item: CartItem) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, cart_item_id: UUID) -> CartItem | None:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, cart_item_id: UUID) -> None:
        raise NotImplementedError()
