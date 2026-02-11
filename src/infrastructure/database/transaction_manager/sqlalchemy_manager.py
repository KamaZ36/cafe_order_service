from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.transaction_manager.base import TransactionManager


class SQLAlchemyTransactionManager(TransactionManager):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self):
        await self._session.commit()
