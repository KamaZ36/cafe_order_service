from uuid import UUID

from sqlalchemy import delete, exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.product import Product

from src.infrastructure.database.models.product import PRODUCT_TABLE
from src.infrastructure.repositories.product.base import BaseProductRepository


class SQLAlchemyProductRepository(BaseProductRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, product: Product) -> None:
        self._session.add(product)

    async def get_by_id(self, product_id: UUID) -> Product | None:
        product = await self._session.get(Product, product_id)
        return product if product else None

    async def check_exist_by_id(self, product_id: UUID) -> bool:
        query = select(exists().where(PRODUCT_TABLE.c.id == product_id))
        result = await self._session.scalar(query)
        return result or False

    async def check_exist_by_name(self, product_name: str) -> bool:
        query = select(exists().where(PRODUCT_TABLE.c.name == product_name))
        result = await self._session.scalar(query)
        return result or False

    async def delete(self, product_id: UUID) -> None:
        stmt = delete(PRODUCT_TABLE).where(PRODUCT_TABLE.c.id == product_id)
        await self._session.execute(stmt)
