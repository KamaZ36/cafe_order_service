from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.product import Product
from src.infrastructure.repositories.product.base import BaseProductRepository


class SQLAlchemyProductRepository(BaseProductRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, product: Product) -> None:
        self._session.add(product)

    async def get_by_id(self, product_id: UUID) -> Product | None:
        product = await self._session.get(Product, product_id)
        return product if product else None
