from sqlalchemy.ext.asyncio import AsyncSession

from typing import AsyncGenerator
from dishka import Provider, provide, Scope

from src.infrastructure.database.transaction_manager.base import TransactionManager
from src.infrastructure.database.transaction_manager.sqlalchemy_manager import (
    SQLAlchemyTransactionManager,
)
from src.infrastructure.database.connection import async_session_maker


class DatabaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def get_transaction_manager(
        self, session: AsyncSession
    ) -> TransactionManager:
        return SQLAlchemyTransactionManager(session)
