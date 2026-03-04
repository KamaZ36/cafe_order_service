from uuid import UUID, uuid4

from infrastructure.database.transaction_manager.base import TransactionManager
from infrastructure.repositories.session.base import BaseSessionRepository

from api.auth.model import AuthSession


class AuthService:
    def __init__(
        self,
        session_repository: BaseSessionRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self._session_repository = session_repository
        self._transaction_manager = transaction_manager

    async def create_user_session(self, user_id: UUID, ip_address: str) -> AuthSession:
        auth_session = AuthSession.create(
            session_id=uuid4(), user_id=user_id, ip_address=ip_address
        )

        await self._session_repository.create(auth_session)
        await self._transaction_manager.commit()

        return auth_session
