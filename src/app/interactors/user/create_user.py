from dataclasses import dataclass
from uuid import UUID, uuid7

from domain.entities.user import User

from app.exceptions.user import UserAlreadyExist

from infrastructure.database.transaction_manager.base import TransactionManager
from infrastructure.repositories.user.base import BaseUserRepository


@dataclass
class CreateUserCommand:
    phone_number: str


class CreateUserInteractor:
    def __init__(
        self,
        user_repository: BaseUserRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self._user_repository = user_repository
        self._transaction_manager = transaction_manager

    async def __call__(self, data: CreateUserCommand) -> UUID:
        is_user_exist = await self._user_repository.check_user_exist_by_phone_number(
            data.phone_number
        )
        if is_user_exist:
            raise UserAlreadyExist()

        user = User(id=uuid7(), phone_number=data.phone_number)

        await self._user_repository.create(user)
        await self._transaction_manager.commit()

        return user.id
