from dataclasses import dataclass
from uuid import UUID

from zernyshko.app.dtos.pagination import Pagination
from zernyshko.app.dtos.product import ResponseProductListDTO
from zernyshko.infrastructure.readers.product.base import ProductReader


@dataclass(frozen=True, eq=False)
class GetProductListQuery:
    pagination: Pagination
    search: str | None = None
    category_id: UUID | None = None


class GetProductListInteractor:
    def __init__(self, product_reader: ProductReader) -> None:
        self._product_reader = product_reader

    async def __call__(self, query: GetProductListQuery) -> ResponseProductListDTO:
        products = await self._product_reader.get_list(
            pagination=query.pagination,
            search=query.search,
            category_id=query.category_id,
        )
        return products
