from fastapi import APIRouter, Request

from zernyshko.api.v1.schemas.payment import YooKassaWebhookSchema
from zernyshko.app.interactors.payment.handle_webhook import (
    HandlePaymentWebhookCommand,
    HandlePaymentWebhookInteractor,
)
from zernyshko.core.dependencies.container import container

router = APIRouter()


@router.post(
    "/yookassa/webhook",
    description="Приём уведомлений от ЮKassa об изменении статуса платежа.",
)
async def yookassa_webhook(request: Request, data: YooKassaWebhookSchema) -> None:
    command = HandlePaymentWebhookCommand(provider_payment_id=data.object.id)
    async with container(context={Request: request}) as context:
        interactor = await context.get(HandlePaymentWebhookInteractor)
        await interactor(command)
