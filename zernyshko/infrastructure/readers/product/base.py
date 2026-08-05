from abc import ABC, abstractmethod
from uuid import UUID

from zernyshko.app.dtos.pagination import Pagination
from zernyshko.app.dtos.product import ResponseProductDTO, ResponseProductListDTO


class ProductReader(ABC):
    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> ResponseProductDTO:
        raise NotImplementedError()

    @abstractmethod
    async def get_list(
        self,
        pagination: Pagination,
        search: str | None = None,
        category_id: UUID | None = None,
    ) -> ResponseProductListDTO:
        raise NotImplementedError()
