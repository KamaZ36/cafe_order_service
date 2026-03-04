from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid7

from app.exceptions.product import ProductWithNameAlreadyExist
from app.dtos.file import FileDTO
from app.services.product import ProductService
from domain.entities.product import Product

from app.interactors.common import AuthenticatedCommand

from infrastructure.database.transaction_manager.base import TransactionManager
from infrastructure.repositories.product.base import BaseProductRepository


@dataclass(frozen=True, eq=False, kw_only=True)
class CreateProductCommand(AuthenticatedCommand):
    name: str
    description: str
    weight: str
    category_id: UUID
    price: Decimal
    is_available: bool = True
    is_popular: bool = False
    is_new: bool = False
    file: FileDTO


class CreateProductInteractor:
    def __init__(
        self,
        product_repository: BaseProductRepository,
        transaction_manager: TransactionManager,
        product_service: ProductService,
    ) -> None:
        self._product_service = product_service
        self._product_repository = product_repository
        self._transaction_manager = transaction_manager

    async def __call__(self, command: CreateProductCommand) -> Product:

        is_exist = await self._product_repository.check_exist_by_name(command.name)
        if is_exist:
            raise ProductWithNameAlreadyExist()

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

        file_key = await self._product_service.save_product_image(
            image=command.file, product_id=product.id
        )

        product.set_image(file_key)

        await self._product_repository.create(product)
        await self._transaction_manager.commit()

        return product
