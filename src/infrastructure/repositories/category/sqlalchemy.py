from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.category import Category
from infrastructure.repositories.category.base import BaseCategoryRepository


class SQLAlchemyCategoryRepository(BaseCategoryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, category: Category) -> None:
        self._session.add(category)
