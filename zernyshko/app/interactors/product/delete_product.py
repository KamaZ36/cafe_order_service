from dataclasses import dataclass
from uuid import UUID

from zernyshko.app.exceptions.auth import AccessDenied
from zernyshko.app.exceptions.product import ProductNotFound
from zernyshko.infrastructure.database.transaction_manager.base import TransactionManager
from zernyshko.infrastructure.file_storage.base import BaseFileStorage
from zernyshko.infrastructure.identity_provider.base import IdentityProvider
from zernyshko.infrastructure.repositories.product.base import ProductRepository


@dataclass(frozen=True, eq=False)
class DeleteProductCommand:
    product_id: UUID


class DeleteProductInteractor:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        product_repository: ProductRepository,
        file_storage: BaseFileStorage,
        transaction_manager: TransactionManager,
    ) -> None:
        self._identity_provider = identity_provider
        self._file_storage = file_storage
        self._product_repoository = product_repository
        self._transaction_manager = transaction_manager

    async def __call__(self, command: DeleteProductCommand) -> None:
        current_user = await self._identity_provider.get_current_user()
        if not current_user.is_staff():
            raise AccessDenied()

        is_exist = await self._product_repoository.check_exist_by_id(command.product_id)
        if not is_exist:
            raise ProductNotFound(product_id=command.product_id)

        await self._product_repoository.delete(command.product_id)
        await self._transaction_manager.commit()
