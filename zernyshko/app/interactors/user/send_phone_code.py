import secrets
from dataclasses import dataclass

from zernyshko.app.dtos.sms import SendSmsDTO
from zernyshko.infrastructure.sms.base import SmsSender
from zernyshko.infrastructure.verification.base import PhoneVerificationCodeStorage

CODE_LENGTH = 6


@dataclass(frozen=True, eq=False)
class SendPhoneVerificationCodeCommand:
    phone_number: str


class SendPhoneVerificationCodeInteractor:
    def __init__(
        self,
        code_storage: PhoneVerificationCodeStorage,
        sms_sender: SmsSender,
    ) -> None:
        self._code_storage = code_storage
        self._sms_sender = sms_sender

    async def __call__(self, command: SendPhoneVerificationCodeCommand) -> None:
        code = self._generate_code()

        await self._code_storage.create(command.phone_number, code)
        await self._sms_sender.send(
            SendSmsDTO(phone_number=command.phone_number, code=code)
        )

    def _generate_code(self) -> str:
        alphabet = "0123456789"
        return "".join(secrets.choice(alphabet) for _ in range(CODE_LENGTH))
