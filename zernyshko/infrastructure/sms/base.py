from abc import ABC, abstractmethod

from zernyshko.app.dtos.sms import SendSmsDTO


class SmsSender(ABC):
    @abstractmethod
    async def send(self, dto: SendSmsDTO) -> None:
        raise NotImplementedError()
