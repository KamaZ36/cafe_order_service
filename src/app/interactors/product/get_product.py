from dataclasses import dataclass
from uuid import UUID

from app.exceptions.product import ProductNotFound
from app.dtos.product import ResponseProductDTO

from infrastructure.readers.product.base import ProductReader
from infrastructure.repositories.product.base import BaseProductRepository


@dataclass(frozen=True, eq=False)
class GetProductByIdQuery:
    product_id: UUID


class GetProductByIdInteractor:
    def __init__(self, product_reader: ProductReader) -> None:
        self._product_reader = product_reader

    async def __call__(self, query: GetProductByIdQuery) -> ResponseProductDTO:
        product = await self._product_reader.get_by_id(query.product_id)
        if product is None:
            raise ProductNotFound(query.product_id)

        return product
