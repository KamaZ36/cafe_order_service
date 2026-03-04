from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.user import User


class BaseUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_phone_number(self, phone_number: str) -> User | None:
        raise NotImplementedError()

    @abstractmethod
    async def check_user_exist_by_phone_number(self, phone_number: str) -> bool:
        raise NotImplementedError()
