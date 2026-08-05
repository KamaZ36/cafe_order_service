from abc import ABC, abstractmethod

from zernyshko.domain.entities.category import Category


class BaseCategoryRepository(ABC):
    @abstractmethod
    async def create(self, category: Category) -> None:
        raise NotADirectoryError()

    @abstractmethod
    async def get_all(self) -> list[Category]:
        raise NotImplementedError()
