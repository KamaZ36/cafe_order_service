from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from zernyshko.app.dtos.file import FileDTO
from zernyshko.app.exceptions.auth import AccessDenied
from zernyshko.app.exceptions.product import ProductNotFound, ProductWithNameAlreadyExist
from zernyshko.app.services.product import ProductService
from zernyshko.domain.entities.product import Product
from zernyshko.infrastructure.database.transaction_manager.base import TransactionManager
from zernyshko.infrastructure.identity_provider.base import IdentityProvider
from zernyshko.infrastructure.repositories.product.base import ProductRepository


@dataclass(frozen=True, eq=False, kw_only=True)
class UpdateProductCommand:
    product_id: UUID
    name: str
    description: str
    weight: str
    category_id: UUID
    price: Decimal
    is_available: bool
    is_popular: bool
    is_new: bool
    composition: str | None = None
    file: FileDTO | None = None


class UpdateProductInteractor:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        product_repository: ProductRepository,
        transaction_manager: TransactionManager,
        product_service: ProductService,
    ) -> None:
        self._identity_provider = identity_provider
        self._product_service = product_service
        self._product_repository = product_repository
        self._transaction_manager = transaction_manager

    async def __call__(self, command: UpdateProductCommand) -> Product:
        current_user = await self._identity_provider.get_current_user()
        if not current_user.is_staff():
            raise AccessDenied()

        product = await self._product_repository.get_by_id(command.product_id)
        if product is None:
            raise ProductNotFound(product_id=command.product_id)

        if product.name != command.name:
            is_exist = await self._product_repository.check_exist_by_name(command.name)
            if is_exist:
                raise ProductWithNameAlreadyExist()

        product.set_name(command.name)
        product.set_description(command.description)
        product.set_weight(command.weight)
        product.set_composition(command.composition)
        product.set_category_id(command.category_id)
        product.set_price(command.price)
        product.set_availability(command.is_available)
        product.set_popular(command.is_popular)
        product.set_new(command.is_new)

        if command.file is not None:
            file_key = await self._product_service.save_product_image(
                image=command.file, product_id=product.id
            )
            product.set_image(file_key)

        await self._transaction_manager.commit()

        return product
