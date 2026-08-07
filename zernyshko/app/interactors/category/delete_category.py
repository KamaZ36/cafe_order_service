from dataclasses import dataclass
from uuid import UUID

from zernyshko.app.exceptions.auth import AccessDenied
from zernyshko.app.exceptions.category import CategoryHasProducts, CategoryNotFound
from zernyshko.infrastructure.database.transaction_manager.base import TransactionManager
from zernyshko.infrastructure.identity_provider.base import IdentityProvider
from zernyshko.infrastructure.repositories.category.base import BaseCategoryRepository
from zernyshko.infrastructure.repositories.product.base import ProductRepository


@dataclass(frozen=True, eq=False)
class DeleteCategoryCommand:
    category_id: UUID


class DeleteCategoryInteractor:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        category_repository: BaseCategoryRepository,
        product_repository: ProductRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self._identity_provider = identity_provider
        self._category_repository = category_repository
        self._product_repository = product_repository
        self._transaction_manager = transaction_manager

    async def __call__(self, command: DeleteCategoryCommand) -> None:
        current_user = await self._identity_provider.get_current_user()
        if not current_user.is_staff():
            raise AccessDenied()

        category = await self._category_repository.get_by_id(command.category_id)
        if category is None:
            raise CategoryNotFound(category_id=command.category_id)

        has_products = await self._product_repository.check_exist_by_category_id(
            command.category_id
        )
        if has_products:
            raise CategoryHasProducts()

        await self._category_repository.delete(command.category_id)
        await self._transaction_manager.commit()
