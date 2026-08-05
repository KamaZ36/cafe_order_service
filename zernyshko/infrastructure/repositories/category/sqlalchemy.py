from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from zernyshko.domain.entities.category import Category
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
