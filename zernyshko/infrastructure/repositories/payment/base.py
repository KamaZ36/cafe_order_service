from abc import ABC, abstractmethod
from uuid import UUID

from zernyshko.domain.entities.payment import Payment


class PaymentRepository(ABC):
    @abstractmethod
    async def create(self, payment: Payment) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, payment_id: UUID) -> Payment | None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_provider_payment_id(
        self, provider_payment_id: str
    ) -> Payment | None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_order_id(self, order_id: UUID) -> Payment | None:
        raise NotImplementedError()
