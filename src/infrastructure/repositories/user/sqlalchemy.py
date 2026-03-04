from uuid import UUID

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.models.user import USER_TABLE
from domain.entities.user import User
from infrastructure.repositories.user.base import BaseUserRepository


class SQLAlchemyUserRepository(BaseUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user: User) -> None:
        self._session.add(user)

    async def get_by_id(self, user_id: UUID) -> User | None:
        user = await self._session.get(User, user_id)
        return user if user else None

    async def get_by_phone_number(self, phone_number: str) -> User | None:
        query = select(User).where(User.phone_number == phone_number)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def check_user_exist_by_phone_number(self, phone_number: str) -> bool:
        query = select(exists().where(USER_TABLE.c.phone_number == phone_number))
        result = await self._session.scalar(query)
        return result or False
