from dataclasses import dataclass
from uuid import UUID

from zernyshko.app.dtos.user import ResponseStaffUserDetailDTO
from zernyshko.app.exceptions.auth import AccessDenied
from zernyshko.app.exceptions.user import UserNotFound
from zernyshko.infrastructure.identity_provider.base import IdentityProvider
from zernyshko.infrastructure.readers.user.base import UserReader


@dataclass(frozen=True, eq=False)
class GetStaffUserDetailQuery:
    user_id: UUID


class GetStaffUserDetailInteractor:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        user_reader: UserReader,
    ) -> None:
        self._identity_provider = identity_provider
        self._user_reader = user_reader

    async def __call__(
        self, query: GetStaffUserDetailQuery
    ) -> ResponseStaffUserDetailDTO:
        current_user = await self._identity_provider.get_current_user()
        if not current_user.is_admin():
            raise AccessDenied()

        user = await self._user_reader.get_detail(query.user_id)
        if user is None:
            raise UserNotFound(user_id=query.user_id)

        return user
