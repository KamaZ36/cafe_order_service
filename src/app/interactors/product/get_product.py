from dataclasses import dataclass
from uuid import UUID

from src.app.exceptions.product import ProductNotFound
from src.app.dtos.product import ResponseProductDTO

from src.infrastructure.repositories.product.base import BaseProductRepository


@dataclass(frozen=True, eq=False)
class GetProductByIdQuery:
    product_id: UUID


class GetProductByIdInteractor:
    def __init__(self, product_repository: BaseProductRepository) -> None:
        self._product_repository = product_repository

    async def __call__(self, query: GetProductByIdQuery) -> ResponseProductDTO:
        product = await self._product_repository.get_by_id(query.product_id)
        if product is None:
            raise ProductNotFound(query.product_id)

        response_dto = ResponseProductDTO(
            name=product.name,
            image=product.image,
            price=product.price,
            is_available=product.is_available,
            is_popular=product.is_popular,
            is_new=product.is_new,
        )

        return response_dto
