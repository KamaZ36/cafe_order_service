from dataclasses import dataclass
from uuid import UUID

from app.exceptions.product import ProductNotFound
from app.interactors.common import AuthenticatedCommand

from infrastructure.database.transaction_manager.base import TransactionManager
from infrastructure.file_storage.base import BaseFileStorage
from infrastructure.repositories.product.base import BaseProductRepository


@dataclass(frozen=True, eq=False)
class DeleteProductCommand(AuthenticatedCommand):
    product_id: UUID


class DeleteProductInteractor:
    def __init__(
        self,
        product_repository: BaseProductRepository,
        file_storage: BaseFileStorage,
        transaction_manager: TransactionManager,
    ) -> None:
        self._file_storage = file_storage
        self._product_repoository = product_repository
        self._transaction_manager = transaction_manager

    async def __call__(self, command: DeleteProductCommand) -> None:
        is_exist = await self._product_repoository.check_exist_by_id(command.product_id)
        if is_exist:
            raise ProductNotFound(product_id=command.product_id)

        await self._product_repoository.delete(command.product_id)
        await self._transaction_manager.commit()
