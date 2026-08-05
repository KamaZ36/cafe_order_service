from zernyshko.domain.entities.user import User
from zernyshko.infrastructure.identity_provider.base import IdentityProvider


class GetCurrentUserInteractor:
    def __init__(self, identity_provider: IdentityProvider) -> None:
        self._identity_provider = identity_provider

    async def __call__(self) -> User:
        return await self._identity_provider.get_current_user()
