from dataclasses import dataclass
from uuid import UUID

from zernyshko.app.exceptions.user import InvalidCredentials
from zernyshko.infrastructure.repositories.user.base import BaseUserRepository
from zernyshko.infrastructure.security.password_hasher import PasswordHasher


@dataclass(frozen=True, eq=False)
class LoginCommand:
    phone_number: str
    password: str


class LoginInteractor:
    def __init__(
        self,
        user_repository: BaseUserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    async def __call__(self, command: LoginCommand) -> UUID:
        user = await self._user_repository.get_by_phone_number(command.phone_number)
        if user is None or user.password_hash is None:
            raise InvalidCredentials()

        if not self._password_hasher.verify(user.password_hash, command.password):
            raise InvalidCredentials()

        return user.id
