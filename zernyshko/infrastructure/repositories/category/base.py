from abc import ABC, abstractmethod
from uuid import UUID

from zernyshko.domain.entities.category import Category


class BaseCategoryRepository(ABC):
    @abstractmethod
    async def create(self, category: Category) -> None:
        raise NotADirectoryError()

    @abstractmethod
    async def get_all(self) -> list[Category]:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, category_id: UUID) -> Category | None:
        raise NotImplementedError()

    @abstractmethod
    async def check_exist_by_name(self, category_name: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, category_id: UUID) -> None:
        raise NotImplementedError()
