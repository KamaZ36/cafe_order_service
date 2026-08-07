from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, eq=False, kw_only=True)
class PaymentInitResult:
    provider_payment_id: str
    confirmation_url: str


@dataclass(frozen=True, eq=False, kw_only=True)
class PaymentStatusResult:
    is_succeeded: bool
    is_canceled: bool


class PaymentGateway(ABC):
    @abstractmethod
    async def create_payment(
        self,
        *,
        payment_id: UUID,
        amount_kopecks: int,
        description: str,
        return_url: str,
    ) -> PaymentInitResult:
        raise NotImplementedError()

    @abstractmethod
    async def get_payment_status(self, provider_payment_id: str) -> PaymentStatusResult:
        raise NotImplementedError()
