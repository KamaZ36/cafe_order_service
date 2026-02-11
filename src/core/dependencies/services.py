from dishka import Provider, provide, Scope

from src.infrastructure.database.transaction_manager.base import TransactionManager
from src.infrastructure.repositories.session.base import BaseSessionRepository
from src.infrastructure.repositories.cart.base import BaseCartRepository
from src.app.services.cart import CartService

from src.api.auth.auth_service import AuthService


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
