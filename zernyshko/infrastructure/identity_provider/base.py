from abc import ABC, abstractmethod
from uuid import UUID

from zernyshko.domain.entities.user import User


class SessionIdGetter(ABC):
    @abstractmethod
    async def get(self) -> UUID | None:
        raise NotImplementedError()


class IdentityProvider(ABC):
    @abstractmethod
    async def get_current_user_id(self) -> UUID:
        raise NotImplementedError()

    @abstractmethod
    async def get_current_user_id_or_none(self) -> UUID | None:
        raise NotImplementedError()

    @abstractmethod
    async def get_current_user(self) -> User:
        raise NotImplementedError()

    @abstractmethod
    async def get_current_session_id(self) -> UUID:
        raise NotImplementedError()
