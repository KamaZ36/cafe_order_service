from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.pagination import Pagination
from app.dtos.product import (
    ResponseProductDTO,
    ResponseProductForListDTO,
    ResponseProductListDTO,
)
from infrastructure.readers.product.base import ProductReader
from infrastructure.database.models.product import PRODUCT_TABLE


class SQLAlchemyProductReader(ProductReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, product_id: UUID) -> ResponseProductDTO:
        query = select(PRODUCT_TABLE).where(PRODUCT_TABLE.c.id == product_id)
        result = await self._session.execute(query)
        row = result.one()
        return ResponseProductDTO(
            name=row.name,
            description=row.description,
            price=row.price,
            image=row.image,
            is_available=row.is_available,
            is_popular=row.is_popular,
            is_new=row.is_new,
        )

    async def get_list(self, pagination: Pagination) -> ResponseProductListDTO:
        count_query = select(func.count()).select_from(PRODUCT_TABLE)
        total_count = await self._session.scalar(count_query)

        query = select(PRODUCT_TABLE).limit(pagination.limit).offset(pagination.offset)
        result = await self._session.execute(query)
        rows = result.all()

        products = [
            ResponseProductForListDTO(
                id=row.id,
                name=row.name,
                image=row.image,
                price=row.price,
                is_available=row.is_available,
                is_popular=row.is_popular,
                is_new=row.is_new,
            )
            for row in rows
        ]

        return ResponseProductListDTO(
            total_count=total_count, count=len(products), products=products
        )
