import logging

from zernyshko.app.dtos.sms import SendSmsDTO
from zernyshko.infrastructure.sms.base import SmsSender

logger = logging.getLogger("zernyshko.sms")


class ConsoleSmsSender(SmsSender):
    """Заглушка на время, пока не подключён реальный SMS-провайдер.

    Просто пишет код в лог вместо отправки настоящей SMS. Использовать
    только для разработки — в проде нужен реальный SmsSender (SMS.ru,
    Twilio и т.п.), иначе клиент никогда не получит код.
    """

    async def send(self, dto: SendSmsDTO) -> None:
        logger.warning(
            "SMS не отправлена (нет провайдера): код %s для номера %s",
            dto.code,
            dto.phone_number,
            extra={"phone_number": dto.phone_number},
        )
