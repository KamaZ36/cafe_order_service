from dataclasses import dataclass
from uuid import UUID

from zernyshko.app.exceptions.auth import AccessDenied
from zernyshko.app.exceptions.category import (
    CategoryNotFound,
    CategoryWithNameAlreadyExist,
)
from zernyshko.domain.entities.category import Category
from zernyshko.infrastructure.database.transaction_manager.base import TransactionManager
from zernyshko.infrastructure.identity_provider.base import IdentityProvider
from zernyshko.infrastructure.repositories.category.base import BaseCategoryRepository


@dataclass(frozen=True, eq=False, kw_only=True)
class UpdateCategoryCommand:
    category_id: UUID
    name: str


class UpdateCategoryInteractor:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        category_repository: BaseCategoryRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self._identity_provider = identity_provider
        self._category_repository = category_repository
        self._transaction_manager = transaction_manager

    async def __call__(self, command: UpdateCategoryCommand) -> Category:
        current_user = await self._identity_provider.get_current_user()
        if not current_user.is_staff():
            raise AccessDenied()

        category = await self._category_repository.get_by_id(command.category_id)
        if category is None:
            raise CategoryNotFound(category_id=command.category_id)

        if category.name != command.name:
            is_exist = await self._category_repository.check_exist_by_name(command.name)
            if is_exist:
                raise CategoryWithNameAlreadyExist()

        category.set_name(command.name)

        await self._transaction_manager.commit()

        return category
