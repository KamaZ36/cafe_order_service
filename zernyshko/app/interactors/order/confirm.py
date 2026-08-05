from dataclasses import dataclass
from uuid import UUID

from zernyshko.app.exceptions.auth import AccessDenied
from zernyshko.app.exceptions.order import OrderNotFound
from zernyshko.infrastructure.database.transaction_manager.base import TransactionManager
from zernyshko.infrastructure.identity_provider.base import IdentityProvider
from zernyshko.infrastructure.repositories.order.base import OrderRepository


@dataclass(frozen=True, eq=False)
class ConfirmOrderCommand:
    order_id: UUID


class ConfirmOrderInteractor:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        order_repository: OrderRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self._identity_provider = identity_provider
        self._order_repository = order_repository
        self._transaction_manager = transaction_manager

    async def __call__(self, command: ConfirmOrderCommand) -> None:
        current_user = await self._identity_provider.get_current_user()
        if not current_user.is_staff():
            raise AccessDenied()

        order = await self._order_repository.get_by_id(command.order_id)
        if order is None:
            raise OrderNotFound(order_id=command.order_id)

        order.confirm()

        await self._transaction_manager.commit()
