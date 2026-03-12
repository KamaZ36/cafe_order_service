from abc import ABC, abstractmethod
from uuid import UUID

from app.dtos.product import ResponseProductDTO


class ProductReader(ABC):
    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> ResponseProductDTO:
        raise NotImplementedError()

    async def get_list(self, offset: int, size: int) -> list[]
