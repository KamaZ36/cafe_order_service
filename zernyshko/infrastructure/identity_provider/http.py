from uuid import UUID

from fastapi import Request

from zernyshko.api.auth.model import AuthSession
from zernyshko.app.exceptions.auth import UnauthorizedError
from zernyshko.domain.entities.user import User
from zernyshko.infrastructure.identity_provider.base import (
    IdentityProvider,
    SessionIdGetter,
)
from zernyshko.infrastructure.repositories.session.base import BaseSessionRepository
from zernyshko.infrastructure.repositories.user.base import BaseUserRepository


class CookieSessionIdGetter(SessionIdGetter):
    def __init__(self, request: Request) -> None:
        self._request = request

    async def get(self) -> UUID | None:
        return self._request.cookies.get("session_id")


class HTTPIdentityProvider(IdentityProvider):
    def __init__(
        self,
        session_id_getter: SessionIdGetter,
        session_repository: BaseSessionRepository,
        user_repository: BaseUserRepository,
    ) -> None:
        self._session_id_getter = session_id_getter
        self._session_repository = session_repository
        self._user_repository = user_repository
        self._active_session: AuthSession | None = None
        self._resolved = False

    async def _get_active_session(self) -> AuthSession | None:
        if self._resolved:
            return self._active_session

        self._resolved = True

        session_id = await self._session_id_getter.get()
        if session_id is None:
            return None

        session = await self._session_repository.get_by_session_id(session_id)
        if session is None or session.is_expired:
            return None

        self._active_session = session
        return session

    async def get_current_user_id(self) -> UUID:
        session = await self._get_active_session()
        if session is None:
            raise UnauthorizedError()

        return session.user_id

    async def get_current_user_id_or_none(self) -> UUID | None:
        session = await self._get_active_session()
        return session.user_id if session else None

    async def get_current_user(self) -> User:
        user_id = await self.get_current_user_id()

        user = await self._user_repository.get_by_id(user_id)
        if user is None:
            raise UnauthorizedError()

        return user

    async def get_current_session_id(self) -> UUID:
        session = await self._get_active_session()
        if session is None:
            raise UnauthorizedError()

        return session.session_id
