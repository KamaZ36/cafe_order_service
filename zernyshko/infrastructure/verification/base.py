from abc import ABC, abstractmethod


class PhoneVerificationCodeStorage(ABC):
    @abstractmethod
    async def create(self, phone_number: str, code: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get(self, phone_number: str) -> str | None:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, phone_number: str) -> None:
        raise NotImplementedError()
