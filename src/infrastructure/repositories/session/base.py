from abc import ABC, abstractmethod
from uuid import UUID

from src.api.auth.model import AuthSession


class BaseSessionRepository(ABC):
    @abstractmethod
    async def create(self, auth_session: AuthSession) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_session_id(self, session_id: UUID) -> AuthSession | None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> AuthSession | None:
        raise NotImplementedError()
