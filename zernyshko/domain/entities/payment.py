from datetime import datetime
from enum import StrEnum, auto
from uuid import UUID, uuid7

from zernyshko.domain.exceptions.payment import InvalidPaymentStatusTransition
from zernyshko.utils import get_datetime_utc_now


class PaymentStatus(StrEnum):
    PENDING = auto()
    CONFIRMED = auto()
    CANCELED = auto()


class Payment:
    def __init__(
        self,
        id: UUID,
        provider_payment_id: str | None,
        user_id: UUID,
        order_id: UUID,
        amount: int,
        status: PaymentStatus,
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        self._id = id
        self._provider_payment_id = provider_payment_id
        self._user_id = user_id
        self._order_id = order_id
        self._amount = amount
        self._status = status
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def create(cls, user_id: UUID, order_id: UUID, amount: int) -> "Payment":
        return cls(
            id=uuid7(),
            provider_payment_id=None,
            user_id=user_id,
            order_id=order_id,
            amount=amount,
            status=PaymentStatus.PENDING,
            created_at=get_datetime_utc_now(),
            updated_at=get_datetime_utc_now(),
        )

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def order_id(self) -> UUID:
        return self._order_id

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def provider_payment_id(self) -> str | None:
        return self._provider_payment_id

    @property
    def status(self) -> PaymentStatus:
        return self._status

    def set_payment_provider_id(self, payment_provider_id: str) -> None:
        self._provider_payment_id = payment_provider_id
        self._updated_at = get_datetime_utc_now()

    def confirm(self) -> None:
        if self._status != PaymentStatus.PENDING:
            raise InvalidPaymentStatusTransition(
                current_status=self._status.value,
                target_status=PaymentStatus.CONFIRMED.value,
            )
        self._status = PaymentStatus.CONFIRMED
        self._updated_at = get_datetime_utc_now()

    def cancel(self) -> None:
        if self._status != PaymentStatus.PENDING:
            raise InvalidPaymentStatusTransition(
                current_status=self._status.value,
                target_status=PaymentStatus.CANCELED.value,
            )
        self._status = PaymentStatus.CANCELED
        self._updated_at = get_datetime_utc_now()
