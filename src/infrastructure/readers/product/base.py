from abc import ABC, abstractmethod
from uuid import UUID

from app.dtos.pagination import Pagination
from app.dtos.product import ResponseProductDTO, ResponseProductListDTO


class ProductReader(ABC):
    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> ResponseProductDTO:
        raise NotImplementedError()

    @abstractmethod
    async def get_list(self, pagination: Pagination) -> ResponseProductListDTO:
        raise NotImplementedError()
