from dataclasses import dataclass
from uuid import UUID, uuid7

from src.domain.entities.category import Category

from src.app.interactors.common import AuthenticatedCommand

from src.infrastructure.database.transaction_manager.base import TransactionManager
from src.infrastructure.repositories.category.base import BaseCategoryRepository


@dataclass(frozen=True, eq=False)
class CreateCategoryCommand(AuthenticatedCommand):
    name: str


class CreateCategoryInteractor:
    def __init__(
        self,
        category_repository: BaseCategoryRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self._category_repository = category_repository
        self._transaction_manager = transaction_manager

    async def __call__(self, command: CreateCategoryCommand) -> Category:
        category = Category(id=uuid7(), name=command.name)
        await self._category_repository.create(category)
        await self._transaction_manager.commit()
