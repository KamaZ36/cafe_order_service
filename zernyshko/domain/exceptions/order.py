from zernyshko.domain.exceptions.base import DomainErrorCode, DomainException


class InvalidOrderStatusTransition(DomainException):
    def __init__(self, current_status: str, target_status: str) -> None:
        super().__init__(
            message=(
                f"Невозможно перевести заказ из статуса {current_status} "
                f"в {target_status}."
            ),
            error_code=DomainErrorCode.INVALID_ORDER_STATUS_TRANSITION,
        )
