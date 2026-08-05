from dataclasses import dataclass

from zernyshko.app.exceptions.auth import AuthCodeNotValid
from zernyshko.infrastructure.verification.base import PhoneVerificationCodeStorage


@dataclass(frozen=True, eq=False)
class VerifyPhoneCodeCommand:
    phone_number: str
    code: str


class VerifyPhoneCodeInteractor:
    def __init__(self, code_storage: PhoneVerificationCodeStorage) -> None:
        self._code_storage = code_storage

    async def __call__(self, command: VerifyPhoneCodeCommand) -> None:
        stored_code = await self._code_storage.get(command.phone_number)

        if stored_code is None or stored_code != command.code:
            raise AuthCodeNotValid()

        await self._code_storage.delete(command.phone_number)
