from zernyshko.infrastructure.database.transaction_manager.base import TransactionManager
from zernyshko.infrastructure.identity_provider.base import IdentityProvider
from zernyshko.infrastructure.repositories.session.base import BaseSessionRepository


class LogoutInteractor:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        session_repository: BaseSessionRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self._identity_provider = identity_provider
        self._session_repository = session_repository
        self._transaction_manager = transaction_manager

    async def __call__(self) -> None:
        session_id = await self._identity_provider.get_current_session_id()

        await self._session_repository.delete(session_id)
        await self._transaction_manager.commit()
