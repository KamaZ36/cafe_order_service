from dishka import Provider, provide, Scope

from app.services.product import ProductService
from infrastructure.file_storage.base import BaseFileStorage
from infrastructure.database.transaction_manager.base import TransactionManager
from infrastructure.repositories.session.base import BaseSessionRepository
from infrastructure.repositories.cart.base import BaseCartRepository
from app.services.cart import CartService

from api.auth.auth_service import AuthService


class ServicesProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_auth_service(
        self,
        auth_session_repository: BaseSessionRepository,
        transaction_manager: TransactionManager,
    ) -> AuthService:
        return AuthService(
            session_repository=auth_session_repository,
            transaction_manager=transaction_manager,
        )

    @provide
    def get_cart_service(self, cart_repository: BaseCartRepository) -> CartService:
        return CartService(cart_repository)

    @provide
    def get_product_service(self, file_storage: BaseFileStorage) -> ProductService:
        return ProductService(file_storage)
