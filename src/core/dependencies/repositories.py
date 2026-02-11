from sqlalchemy.ext.asyncio import AsyncSession

from dishka import Provider, provide, Scope

from src.infrastructure.repositories.session.base import BaseSessionRepository
from src.infrastructure.repositories.category.base import BaseCategoryRepository
from src.infrastructure.repositories.product.base import BaseProductRepository
from src.infrastructure.repositories.cart.base import BaseCartRepository
from src.infrastructure.repositories.user.base import BaseUserRepository

from src.infrastructure.repositories.session.sqlalchemy import (
    SQLAlchemySessionRepository,
)
from src.infrastructure.repositories.category.sqlalchemy import (
    SQLAlchemyCategoryRepository,
)
from src.infrastructure.repositories.product.sqlalchemy import (
    SQLAlchemyProductRepository,
)
from src.infrastructure.repositories.cart.sqlalchemy import SQLAlchemyCartRepository
from src.infrastructure.repositories.user.sqlalchemy import SQLAlchemyUserRepository


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_user_repository(self, session: AsyncSession) -> BaseUserRepository:
        return SQLAlchemyUserRepository(session)

    @provide
    def get_cart_repository(self, session: AsyncSession) -> BaseCartRepository:
        return SQLAlchemyCartRepository(session)

    @provide
    def get_product_repository(self, session: AsyncSession) -> BaseProductRepository:
        return SQLAlchemyProductRepository(session)

    @provide
    def get_category_repository(self, session: AsyncSession) -> BaseCategoryRepository:
        return SQLAlchemyCategoryRepository(session)

    @provide
    def get_auth_session_repository(
        self, session: AsyncSession
    ) -> BaseSessionRepository:
        return SQLAlchemySessionRepository(session)
