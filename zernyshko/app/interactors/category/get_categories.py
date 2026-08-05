from zernyshko.domain.entities.category import Category
from zernyshko.infrastructure.repositories.category.base import BaseCategoryRepository


class GetCategoryListInteractor:
    def __init__(self, category_repository: BaseCategoryRepository) -> None:
        self._category_repository = category_repository

    async def __call__(self) -> list[Category]:
        return await self._category_repository.get_all()
