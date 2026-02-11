from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.product import Product


class BaseProductRepository(ABC):
    @abstractmethod
    async def create(self, product: Product) -> None:
        raise NotADirectoryError()

    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> Product | None:
        raise NotImplementedError()
