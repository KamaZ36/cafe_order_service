from abc import ABC, abstractmethod

from domain.entities.category import Category


class BaseCategoryRepository(ABC):
    @abstractmethod
    async def create(self, category: Category) -> None:
        raise NotADirectoryError()
