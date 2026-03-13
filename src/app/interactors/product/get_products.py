from dataclasses import dataclass

from app.dtos.pagination import Pagination
from app.dtos.product import ResponseProductListDTO
from infrastructure.readers.product.base import ProductReader


@dataclass(frozen=True, eq=False)
class GetProductListQuery:
    pagination: Pagination


class GetProductListInteractor:
    def __init__(self, product_reader: ProductReader) -> None:
        self._product_reader = product_reader

    async def __call__(self, query: GetProductListQuery) -> ResponseProductListDTO:
        products = await self._product_reader.get_list(pagination=query.pagination)
        return products
