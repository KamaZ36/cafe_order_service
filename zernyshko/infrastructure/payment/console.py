import logging
from uuid import UUID

from zernyshko.infrastructure.payment.base import (
    PaymentGateway,
    PaymentInitResult,
    PaymentStatusResult,
)

logger = logging.getLogger("zernyshko.payments")


class ConsolePaymentGateway(PaymentGateway):
    """Заглушка на время, пока не настроен реальный магазин в ЮKassa.

    Не делает сетевых запросов: "оплата" считается сразу доступной к
    подтверждению через вебхук. Использовать только для разработки и
    тестов — в проде нужен настоящий YooKassaPaymentGateway с реальными
    shop_id/secret_key, иначе деньги никто не спишет.
    """

    async def create_payment(
        self,
        *,
        payment_id: UUID,
        amount_kopecks: int,
        description: str,
        return_url: str,
    ) -> PaymentInitResult:
        provider_payment_id = f"console-{payment_id}"
        logger.warning(
            "Платёж не создан в ЮKassa (нет провайдера): %s на %s коп. (%s)",
            provider_payment_id,
            amount_kopecks,
            description,
        )
        return PaymentInitResult(
            provider_payment_id=provider_payment_id,
            confirmation_url=return_url,
        )

    async def get_payment_status(self, provider_payment_id: str) -> PaymentStatusResult:
        return PaymentStatusResult(is_succeeded=True, is_canceled=False)
