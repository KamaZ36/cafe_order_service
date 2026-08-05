from zernyshko.app.dtos.sms import SendSmsDTO
from zernyshko.infrastructure.sms.base import SmsSender


class UnconfiguredSmsSender(SmsSender):
    """Используется, когда debug=False, а реальный SMS-провайдер ещё не
    подключён. Падает громко и явно вместо того, чтобы тихо делать вид,
    что SMS отправлена — так это невозможно не заметить в проде."""

    async def send(self, dto: SendSmsDTO) -> None:
        raise RuntimeError(
            "Не настроен провайдер SMS для прода. ConsoleSmsSender можно "
            "использовать только при debug=True — подключите реальный "
            "провайдер (SMS.ru, Twilio и т.п.) перед деплоем."
        )
