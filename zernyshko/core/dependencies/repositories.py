from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from zernyshko.infrastructure.repositories.cart.base import BaseCartRepository
from zernyshko.infrastructure.repositories.cart.sqlalchemy import SQLAlchemyCartRepository
from zernyshko.infrastructure.repositories.category.base import BaseCategoryRepository
from zernyshko.infrastructure.repositories.category.sqlalchemy import (
    SQLAlchemyCategoryRepository,
)
from zernyshko.infrastructure.repositories.order.base import OrderRepository
from zernyshko.infrastructure.repositories.order.sqlalchemy import (
    SQLAlchemyOrderRepository,
)
from zernyshko.infrastructure.repositories.payment.base import PaymentRepository
from zernyshko.infrastructure.repositories.payment.sqlalchemy import (
    SQLAlchemyPaymentRepository,
)
from zernyshko.infrastructure.repositories.product.base import ProductRepository
from zernyshko.infrastructure.repositories.product.sqlalchemy import (
    SQLAlchemyProductRepository,
)
from zernyshko.infrastructure.repositories.session.base import BaseSessionRepository
from zernyshko.infrastructure.repositories.session.sqlalchemy import (
    SQLAlchemySessionRepository,
)
from zernyshko.infrastructure.repositories.user.base import BaseUserRepository
from zernyshko.infrastructure.repositories.user.sqlalchemy import SQLAlchemyUserRepository


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_user_repository(self, session: AsyncSession) -> BaseUserRepository:
        return SQLAlchemyUserRepository(session)

    @provide
    def get_cart_repository(self, session: AsyncSession) -> BaseCartRepository:
        return SQLAlchemyCartRepository(session)

    @provide
    def get_product_repository(self, session: AsyncSession) -> ProductRepository:
        return SQLAlchemyProductRepository(session)

    @provide
    def get_category_repository(self, session: AsyncSession) -> BaseCategoryRepository:
        return SQLAlchemyCategoryRepository(session)

    @provide
    def get_order_repository(self, session: AsyncSession) -> OrderRepository:
        return SQLAlchemyOrderRepository(session)

    @provide
    def get_auth_session_repository(self, session: AsyncSession) -> BaseSessionRepository:
        return SQLAlchemySessionRepository(session)

    @provide
    def get_payment_repository(self, session: AsyncSession) -> PaymentRepository:
        return SQLAlchemyPaymentRepository(session)
