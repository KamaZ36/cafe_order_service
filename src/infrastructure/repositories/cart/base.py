from abc import ABC, abstractmethod

from domain.entities.cart import CartItem


class BaseCartItemRepository(ABC):
    @abstractmethod
    async def create(self, cart_item: CartItem) -> None:
        raise NotImplementedError()
