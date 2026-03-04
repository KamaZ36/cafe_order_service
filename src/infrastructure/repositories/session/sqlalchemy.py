from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.model import AuthSession
from infrastructure.repositories.session.base import BaseSessionRepository


class SQLAlchemySessionRepository(BaseSessionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, auth_session: AuthSession) -> None:
        self._session.add(auth_session)

    async def get_by_session_id(self, session_id: UUID) -> AuthSession | None:
        auth_session = await self._session.get(AuthSession, session_id)
        return auth_session if auth_session else None

    async def get_by_user_id(self, user_id: UUID) -> AuthSession | None:
        query = select(AuthSession).where(AuthSession.user_id == user_id)
        result = await self._session.execute(query)
        auth_session = result.scalar_one_or_none()
        return auth_session
