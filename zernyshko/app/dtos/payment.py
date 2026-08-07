from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from zernyshko.domain.entities.payment import PaymentStatus


@dataclass(frozen=True, eq=False, kw_only=True)
class ResponsePaymentDTO:
    id: UUID
    order_id: UUID
    order_number: str
    amount: int
    status: PaymentStatus
    created_at: datetime


@dataclass(frozen=True, eq=False, kw_only=True)
class ResponsePaymentListDTO:
    total_count: int
    count: int
    payments: list[ResponsePaymentDTO]
