import logging
from dataclasses import dataclass

from zernyshko.app.exceptions.payment import PaymentNotFound
from zernyshko.domain.entities.payment import PaymentStatus
from zernyshko.domain.exceptions.order import InvalidOrderStatusTransition
from zernyshko.infrastructure.database.transaction_manager.base import TransactionManager
from zernyshko.infrastructure.payment.base import PaymentGateway
from zernyshko.infrastructure.repositories.order.base import OrderRepository
from zernyshko.infrastructure.repositories.payment.base import PaymentRepository

logger = logging.getLogger("zernyshko.payments")


@dataclass(frozen=True, eq=False)
class HandlePaymentWebhookCommand:
    provider_payment_id: str


class HandlePaymentWebhookInteractor:
    def __init__(
        self,
        payment_repository: PaymentRepository,
        order_repository: OrderRepository,
        payment_gateway: PaymentGateway,
        transaction_manager: TransactionManager,
    ) -> None:
        self._payment_repository = payment_repository
        self._order_repository = order_repository
        self._payment_gateway = payment_gateway
        self._transaction_manager = transaction_manager

    async def __call__(self, command: HandlePaymentWebhookCommand) -> None:
        payment = await self._payment_repository.get_by_provider_payment_id(
            command.provider_payment_id
        )
        if payment is None:
            raise PaymentNotFound(provider_payment_id=command.provider_payment_id)

        # Уже обработан — вебхуки от ЮKassa могут дублироваться, это ок.
        if payment.status != PaymentStatus.PENDING:
            return

        # Тело вебхука не доверенное — перепроверяем статус напрямую в ЮKassa.
        status_result = await self._payment_gateway.get_payment_status(
            command.provider_payment_id
        )

        if status_result.is_succeeded:
            payment.confirm()
            order = await self._order_repository.get_by_id(payment.order_id)
            if order is not None:
                try:
                    order.mark_paid()
                except InvalidOrderStatusTransition:
                    # Заказ уже отменён (клиентом/персоналом), а оплата всё
                    # равно прошла по старой ссылке. Деньги списаны, но в
                    # очередь заказ не пускаем — платёж фиксируем как
                    # подтверждённый, дальше это ручной возврат персоналом.
                    logger.warning(
                        "Payment %s succeeded for order %s in non-payable status %s",
                        command.provider_payment_id,
                        order.id,
                        order.status.value,
                    )
        elif status_result.is_canceled:
            payment.cancel()
        else:
            return

        await self._transaction_manager.commit()
