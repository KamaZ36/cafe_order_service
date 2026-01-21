from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.cart import Cart, CartItem


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
    async def get_cart_items(self, cart_id: UUID) -> list[CartItem]:
        raise NotImplementedError()

    @abstractmethod
    async def get_cart_item_by_id(
        self, cart_id: UUID, item_id: UUID
    ) -> CartItem | None:
        raise NotImplementedError()

    @abstractmethod
    async def get_cart_item_by_product_id(
        self, cart_id: UUID, product_id: UUID
    ) -> CartItem | None:
        raise NotImplementedError()

    @abstractmethod
    async def add_item(self, cart_id: UUID, cart_item: CartItem) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def update_cart_item(self, cart_item: CartItem) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_session_id(self, session_id: UUID) -> Cart | None:
        raise NotImplementedError()

    @abstractmethod
    async def delete_item(self, cart_id: UUID, item_id: UUID) -> None:
        await NotImplementedError()
