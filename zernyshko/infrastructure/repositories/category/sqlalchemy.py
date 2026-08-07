from uuid import UUID

from sqlalchemy import delete, exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from zernyshko.domain.entities.category import Category
from zernyshko.infrastructure.database.models.category import CATEGORY_TABLE
from zernyshko.infrastructure.repositories.category.base import BaseCategoryRepository


class SQLAlchemyCategoryRepository(BaseCategoryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, category: Category) -> None:
        self._session.add(category)

    async def get_all(self) -> list[Category]:
        query = select(Category)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, category_id: UUID) -> Category | None:
        category = await self._session.get(Category, category_id)
        return category if category else None

    async def check_exist_by_name(self, category_name: str) -> bool:
        query = select(exists().where(CATEGORY_TABLE.c.name == category_name))
        result = await self._session.scalar(query)
        return result or False

    async def delete(self, category_id: UUID) -> None:
        stmt = delete(Category).where(CATEGORY_TABLE.c.id == category_id)
        await self._session.execute(stmt)
