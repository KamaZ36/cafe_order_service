import logging
from dataclasses import dataclass
from uuid import UUID

from zernyshko.app.exceptions.auth import AccessDenied
from zernyshko.app.exceptions.order import OrderNotFound
from zernyshko.app.exceptions.payment import PaymentNotFoundForOrder
from zernyshko.core.config import settings
from zernyshko.domain.entities.payment import PaymentStatus
from zernyshko.domain.exceptions.order import InvalidOrderStatusTransition
from zernyshko.infrastructure.database.transaction_manager.base import TransactionManager
from zernyshko.infrastructure.identity_provider.base import IdentityProvider
from zernyshko.infrastructure.repositories.order.base import OrderRepository
from zernyshko.infrastructure.repositories.payment.base import PaymentRepository

logger = logging.getLogger("zernyshko.payments")


@dataclass(frozen=True, eq=False)
class SimulateOrderPaymentCommand:
    order_id: UUID


class SimulateOrderPaymentInteractor:
    """Тестовая кнопка «Оплатить» на время, пока не подключён боевой мерчант
    ЮKassa: подтверждает оплату напрямую, без похода на страницу оплаты.
    Работает только при debug=True — в проде оплату подтверждает
    исключительно вебхук от платёжного провайдера (см. HandlePaymentWebhookInteractor),
    иначе любой клиент мог бы «оплачивать» заказы бесплатно.
    """

    def __init__(
        self,
        identity_provider: IdentityProvider,
        order_repository: OrderRepository,
        payment_repository: PaymentRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self._identity_provider = identity_provider
        self._order_repository = order_repository
        self._payment_repository = payment_repository
        self._transaction_manager = transaction_manager

    async def __call__(self, command: SimulateOrderPaymentCommand) -> None:
        if not settings.debug:
            raise AccessDenied()

        user_id = await self._identity_provider.get_current_user_id()

        order = await self._order_repository.get_by_id(command.order_id)
        if order is None or order.user_id != user_id:
            raise OrderNotFound(order_id=command.order_id)

        payment = await self._payment_repository.get_by_order_id(order.id)
        if payment is None:
            raise PaymentNotFoundForOrder(order_id=order.id)

        # Идемпотентно — повторный клик или гонка с уже пришедшим вебхуком не страшны
        if payment.status != PaymentStatus.PENDING:
            return

        payment.confirm()

        try:
            order.mark_paid()
        except InvalidOrderStatusTransition:
            logger.warning(
                "Simulated payment for order %s in non-payable status %s",
                order.id,
                order.status.value,
            )

        await self._transaction_manager.commit()
