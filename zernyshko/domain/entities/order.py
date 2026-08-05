from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from zernyshko.domain.entities.mixins import CreatedAtMixin
from zernyshko.domain.entities.order_item import OrderItem
from zernyshko.domain.exceptions.order import InvalidOrderStatusTransition


class OrderType(str, Enum):
    PICKUP = "PICKUP"
    DELIVERY = "DELIVERY"


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    READY = "READY"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Order(CreatedAtMixin):
    def __init__(
        self,
        id: UUID,
        order_number: str,
        user_id: UUID,
        order_type: OrderType,
        desired_time: datetime,
        total_amount: Decimal,
        items: list[OrderItem] | None = None,
        status: OrderStatus = OrderStatus.PENDING,
        delivery_address: str | None = None,
        delivery_entrance: str | None = None,
        delivery_floor: int | None = None,
        delivery_intercom: str | None = None,
        comment: str | None = None,
        created_at: datetime | None = None,
        cancel_reason: str | None = None,
    ) -> None:
        CreatedAtMixin.__init__(self, created_at)
        self._id = id
        self._order_number = order_number
        self._user_id = user_id
        self._items = items if items is not None else []
        self._order_type = order_type
        self._status = status
        self._desired_time = desired_time
        self._total_amount = total_amount
        self._delivery_address = delivery_address
        self._delivery_entrance = delivery_entrance
        self._delivery_floor = delivery_floor
        self._delivery_intercom = delivery_intercom
        self._comment = comment
        self._cancel_reason = cancel_reason

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def order_number(self) -> str:
        return self._order_number

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def items(self) -> list[OrderItem]:
        return self._items

    @property
    def order_type(self) -> OrderType:
        return self._order_type

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def desired_time(self) -> datetime:
        return self._desired_time

    @property
    def total_amount(self) -> Decimal:
        return self._total_amount

    @property
    def delivery_address(self) -> str | None:
        return self._delivery_address

    @property
    def delivery_entrance(self) -> str | None:
        return self._delivery_entrance

    @property
    def delivery_floor(self) -> int | None:
        return self._delivery_floor

    @property
    def delivery_intercom(self) -> str | None:
        return self._delivery_intercom

    @property
    def comment(self) -> str | None:
        return self._comment

    @property
    def cancel_reason(self) -> str | None:
        return self._cancel_reason

    # Отменить можно из любого нетерминального статуса — причины бывают
    # на любом этапе (не пришёл, нет в наличии, проблема с оплатой).
    # Более узкое правило "только пока PENDING" для самостоятельной отмены
    # клиентом живёт на уровне интерактора, не здесь.
    _CANCELLABLE_STATUSES = (OrderStatus.PENDING, OrderStatus.CONFIRMED, OrderStatus.READY)

    def cancel(self, reason: str | None = None) -> None:
        if self._status not in self._CANCELLABLE_STATUSES:
            raise InvalidOrderStatusTransition(
                current_status=self._status.value,
                target_status=OrderStatus.CANCELLED.value,
            )
        self._status = OrderStatus.CANCELLED
        self._cancel_reason = reason

    def confirm(self) -> None:
        if self._status != OrderStatus.PENDING:
            raise InvalidOrderStatusTransition(
                current_status=self._status.value,
                target_status=OrderStatus.CONFIRMED.value,
            )
        self._status = OrderStatus.CONFIRMED

    def mark_ready(self) -> None:
        if self._status != OrderStatus.CONFIRMED:
            raise InvalidOrderStatusTransition(
                current_status=self._status.value,
                target_status=OrderStatus.READY.value,
            )
        self._status = OrderStatus.READY

    def complete(self) -> None:
        if self._status != OrderStatus.READY:
            raise InvalidOrderStatusTransition(
                current_status=self._status.value,
                target_status=OrderStatus.COMPLETED.value,
            )
        self._status = OrderStatus.COMPLETED
