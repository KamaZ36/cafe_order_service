from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.product import Product


class BaseProductRepository(ABC):
    @abstractmethod
    async def create(self, product: Product) -> None:
        raise NotADirectoryError()

    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> Product | None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_ids(self, product_ids: list[UUID]) -> list[Product]:
        raise NotImplementedError()

    @abstractmethod
    async def check_exist_by_id(self, product_id: UUID) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def check_exist_by_name(self, product_name: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, product_id: UUID) -> None:
        raise NotImplementedError()
