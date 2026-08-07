from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from zernyshko.app.dtos.pagination import Pagination
from zernyshko.app.dtos.product import (
    ResponseProductDTO,
    ResponseProductForListDTO,
    ResponseProductListDTO,
)
from zernyshko.infrastructure.database.models.product import PRODUCT_TABLE
from zernyshko.infrastructure.readers.product.base import ProductReader


class SQLAlchemyProductReader(ProductReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, product_id: UUID) -> ResponseProductDTO:
        query = select(PRODUCT_TABLE).where(PRODUCT_TABLE.c.id == product_id)
        result = await self._session.execute(query)
        row = result.one()
        return ResponseProductDTO(
            id=row.id,
            name=row.name,
            description=row.description,
            weight=row.weight,
            composition=row.composition,
            category_id=row.category_id,
            price=row.price,
            image=row.image,
            is_available=row.is_available,
            is_popular=row.is_popular,
            is_new=row.is_new,
        )

    async def get_list(
        self,
        pagination: Pagination,
        search: str | None = None,
        category_id: UUID | None = None,
    ) -> ResponseProductListDTO:
        filters = []
        if search:
            pattern = f"%{search}%"
            filters.append(
                PRODUCT_TABLE.c.name.ilike(pattern)
                | PRODUCT_TABLE.c.description.ilike(pattern)
            )
        if category_id:
            filters.append(PRODUCT_TABLE.c.category_id == category_id)

        count_query = select(func.count()).select_from(PRODUCT_TABLE).where(*filters)
        total_count = await self._session.scalar(count_query)

        query = (
            select(PRODUCT_TABLE)
            .where(*filters)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        result = await self._session.execute(query)
        rows = result.all()

        products = [
            ResponseProductForListDTO(
                id=row.id,
                name=row.name,
                image=row.image,
                price=row.price,
                category_id=row.category_id,
                is_available=row.is_available,
                is_popular=row.is_popular,
                is_new=row.is_new,
            )
            for row in rows
        ]

        return ResponseProductListDTO(
            total_count=total_count, count=len(products), products=products
        )
