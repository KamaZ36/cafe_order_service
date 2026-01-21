from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.product import Product


class BaseProductRepository(ABC):
    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> Product | None:
        raise NotImplementedError()
