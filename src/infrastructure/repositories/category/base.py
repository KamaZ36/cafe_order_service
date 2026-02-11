from abc import ABC, abstractmethod

from src.domain.entities.category import Category


class BaseCategoryRepository(ABC):
    @abstractmethod
    async def create(self, category: Category) -> None:
        raise NotADirectoryError()
