from dataclasses import dataclass
from uuid import UUID, uuid7

from zernyshko.domain.entities.user import User, UserRole
from zernyshko.infrastructure.database.transaction_manager.base import TransactionManager
from zernyshko.infrastructure.repositories.user.base import BaseUserRepository
from zernyshko.infrastructure.security.password_hasher import PasswordHasher


@dataclass(frozen=True, eq=False)
class ProvisionStaffCommand:
    phone_number: str
    password: str
    role: UserRole


class ProvisionStaffInteractor:
    def __init__(
        self,
        user_repository: BaseUserRepository,
        password_hasher: PasswordHasher,
        transaction_manager: TransactionManager,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._transaction_manager = transaction_manager

    async def __call__(self, command: ProvisionStaffCommand) -> UUID:
        password_hash = self._password_hasher.hash(command.password)

        user = await self._user_repository.get_by_phone_number(command.phone_number)
        if user is None:
            user = User(id=uuid7(), phone_number=command.phone_number)
            user.promote_to_staff(role=command.role, password_hash=password_hash)
            await self._user_repository.create(user)
        else:
            user.promote_to_staff(role=command.role, password_hash=password_hash)

        await self._transaction_manager.commit()

        return user.id
