from dataclasses import dataclass
from uuid import UUID

from zernyshko.domain.entities.user import User
from zernyshko.infrastructure.database.transaction_manager.base import TransactionManager
from zernyshko.infrastructure.identity_provider.base import IdentityProvider
from zernyshko.infrastructure.repositories.user.base import BaseUserRepository


@dataclass(frozen=True, eq=False)
class ResolvePhoneUserCommand:
    phone_number: str


class ResolvePhoneUserInteractor:
    """Определяет, кем становится текущий запрос после подтверждения телефона:

    - если телефон уже принадлежит существующему пользователю — возвращает
      его id (эндпоинт залогинит в этот аккаунт, выдав новую сессию);
    - если есть текущая (в т.ч. анонимная) сессия — привязывает телефон к
      её пользователю;
    - иначе создаёт нового пользователя с этим телефоном.
    """

    def __init__(
        self,
        identity_provider: IdentityProvider,
        user_repository: BaseUserRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self._identity_provider = identity_provider
        self._user_repository = user_repository
        self._transaction_manager = transaction_manager

    async def __call__(self, command: ResolvePhoneUserCommand) -> UUID:
        existing_user = await self._user_repository.get_by_phone_number(
            command.phone_number
        )
        if existing_user is not None:
            return existing_user.id

        current_user_id = await self._identity_provider.get_current_user_id_or_none()
        if current_user_id is not None:
            current_user = await self._user_repository.get_by_id(current_user_id)
            if current_user is not None:
                current_user.set_phone_number(command.phone_number)
                await self._transaction_manager.commit()
                return current_user.id

        new_user = User.create(phone_number=command.phone_number)
        await self._user_repository.create(new_user)
        await self._transaction_manager.commit()
        return new_user.id
