from dataclasses import dataclass

from zernyshko.app.dtos.pagination import Pagination
from zernyshko.app.dtos.user import ResponseStaffUserListDTO
from zernyshko.app.exceptions.auth import AccessDenied
from zernyshko.infrastructure.identity_provider.base import IdentityProvider
from zernyshko.infrastructure.readers.user.base import UserReader


@dataclass(frozen=True, eq=False)
class GetStaffUserListQuery:
    pagination: Pagination


class GetStaffUserListInteractor:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        user_reader: UserReader,
    ) -> None:
        self._identity_provider = identity_provider
        self._user_reader = user_reader

    async def __call__(self, query: GetStaffUserListQuery) -> ResponseStaffUserListDTO:
        current_user = await self._identity_provider.get_current_user()
        # Список пользователей и их платежей — не общая зона персонала,
        # в отличие от заказов/меню. Доступ только у ADMIN, MANAGER сюда
        # не пускаем (см. User.is_admin).
        if not current_user.is_admin():
            raise AccessDenied()

        return await self._user_reader.get_list(pagination=query.pagination)
