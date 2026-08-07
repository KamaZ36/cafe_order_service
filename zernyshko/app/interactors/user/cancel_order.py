from dataclasses import dataclass
from uuid import UUID

from zernyshko.app.exceptions.order import OrderNotFound
from zernyshko.domain.entities.order import OrderStatus
from zernyshko.domain.exceptions.order import InvalidOrderStatusTransition
from zernyshko.infrastructure.database.transaction_manager.base import TransactionManager
from zernyshko.infrastructure.identity_provider.base import IdentityProvider
from zernyshko.infrastructure.repositories.order.base import OrderRepository


@dataclass(frozen=True, eq=False)
class CancelOrderCommand:
    order_id: UUID


class CancelOrderInteractor:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        order_repository: OrderRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self._identity_provider = identity_provider
        self._order_repository = order_repository
        self._transaction_manager = transaction_manager

    async def __call__(self, command: CancelOrderCommand) -> None:
        user_id = await self._identity_provider.get_current_user_id()

        order = await self._order_repository.get_by_id(command.order_id)
        if order is None or order.user_id != user_id:
            raise OrderNotFound(order_id=command.order_id)

        # Самостоятельная отмена клиентом — пока не оплачен или пока
        # заведение не начало готовить заказ. Дальше отменить может только
        # персонал (см. StaffCancelOrderInteractor) — домен сам по себе
        # разрешает отмену и из CONFIRMED/READY, это ограничение специфично
        # для клиента.
        if order.status not in (OrderStatus.AWAITING_PAYMENT, OrderStatus.PENDING):
            raise InvalidOrderStatusTransition(
                current_status=order.status.value,
                target_status=OrderStatus.CANCELLED.value,
            )

        order.cancel()

        await self._transaction_manager.commit()
