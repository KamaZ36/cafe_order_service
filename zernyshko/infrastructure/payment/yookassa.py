from uuid import UUID

import httpx

from zernyshko.infrastructure.payment.base import (
    PaymentGateway,
    PaymentInitResult,
    PaymentStatusResult,
)

_SUCCEEDED_STATUSES = frozenset({"succeeded", "waiting_for_capture"})
_CANCELED_STATUSES = frozenset({"canceled"})


def _kopecks_to_rubles_str(amount_kopecks: int) -> str:
    rubles, kopecks = divmod(amount_kopecks, 100)
    return f"{rubles}.{kopecks:02d}"


class YooKassaPaymentGateway(PaymentGateway):
    """Прямые запросы к REST API ЮKassa (https://yookassa.ru/developers/api).

    Без официального SDK — он синхронный (на requests), а всё остальное
    приложение асинхронное; здесь используется общий httpx.AsyncClient.
    """

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self._http_client = http_client

    async def create_payment(
        self,
        *,
        payment_id: UUID,
        amount_kopecks: int,
        description: str,
        return_url: str,
    ) -> PaymentInitResult:
        response = await self._http_client.post(
            "/v3/payments",
            headers={"Idempotence-Key": str(payment_id)},
            json={
                "amount": {
                    "value": _kopecks_to_rubles_str(amount_kopecks),
                    "currency": "RUB",
                },
                "confirmation": {"type": "redirect", "return_url": return_url},
                "capture": True,
                "description": description,
            },
        )
        response.raise_for_status()
        data = response.json()
        return PaymentInitResult(
            provider_payment_id=data["id"],
            confirmation_url=data["confirmation"]["confirmation_url"],
        )

    async def get_payment_status(self, provider_payment_id: str) -> PaymentStatusResult:
        response = await self._http_client.get(f"/v3/payments/{provider_payment_id}")
        response.raise_for_status()
        status = response.json()["status"]
        return PaymentStatusResult(
            is_succeeded=status in _SUCCEEDED_STATUSES,
            is_canceled=status in _CANCELED_STATUSES,
        )
