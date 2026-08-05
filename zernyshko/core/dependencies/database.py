from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from zernyshko.core.config import settings
from zernyshko.infrastructure.database.connection import async_session_maker
from zernyshko.infrastructure.database.transaction_manager.base import TransactionManager
from zernyshko.infrastructure.database.transaction_manager.sqlalchemy_manager import (
    SQLAlchemyTransactionManager,
)


class DatabaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def get_transaction_manager(self, session: AsyncSession) -> TransactionManager:
        return SQLAlchemyTransactionManager(session)

    @provide(scope=Scope.APP)
    def get_redis_client(self) -> Redis:
        return Redis.from_url(settings.redis_url)
