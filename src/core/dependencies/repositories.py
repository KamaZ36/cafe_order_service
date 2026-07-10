from sqlalchemy.ext.asyncio import AsyncSession

from dishka import Provider, provide, Scope

from infrastructure.repositories.order.base import OrderRepository
from infrastructure.repositories.order.sqlalchemy import SQLAlchemyOrderRepository
from infrastructure.repositories.session.base import BaseSessionRepository
from infrastructure.repositories.category.base import BaseCategoryRepository
from infrastructure.repositories.product.base import ProductRepository
from infrastructure.repositories.cart.base import BaseCartRepository
from infrastructure.repositories.user.base import BaseUserRepository

from infrastructure.repositories.session.sqlalchemy import (
    SQLAlchemySessionRepository,
)
from infrastructure.repositories.category.sqlalchemy import (
    SQLAlchemyCategoryRepository,
)
from infrastructure.repositories.product.sqlalchemy import (
    SQLAlchemyProductRepository,
)
from infrastructure.repositories.cart.sqlalchemy import SQLAlchemyCartRepository
from infrastructure.repositories.user.sqlalchemy import SQLAlchemyUserRepository


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
    def get_auth_session_repository(
        self, session: AsyncSession
    ) -> BaseSessionRepository:
        return SQLAlchemySessionRepository(session)
