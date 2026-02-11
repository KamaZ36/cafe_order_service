from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid7

from src.domain.entities.product import Product

from src.app.interactors.common import AuthenticatedCommand

from src.infrastructure.database.transaction_manager.base import TransactionManager
from src.infrastructure.repositories.product.base import BaseProductRepository


@dataclass(frozen=True, eq=False)
class CreateProductCommand(AuthenticatedCommand):
    name: str
    description: str
    weight: str
    category_id: UUID
    price: Decimal
    is_available: bool = True
    is_popular: bool = False
    is_new: bool = False


class CreateProductInteractor:
    def __init__(
        self,
        product_repository: BaseProductRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self._product_repository = product_repository
        self._transaction_manager = transaction_manager

    async def __call__(self, command: CreateProductCommand) -> Product:
        product = Product(
            id=uuid7(),
            name=command.name,
            description=command.description,
            weight=command.weight,
            category_id=command.category_id,
            price=command.price,
            is_available=command.is_available,
            is_popular=command.is_popular,
            is_new=command.is_new,
        )
        await self._product_repository.create(product)
        await self._transaction_manager.commit()

        return product
