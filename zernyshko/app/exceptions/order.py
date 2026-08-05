from uuid import UUID

from zernyshko.app.exceptions.base import AppErrorCode, AppException


class OrderNotFound(AppException):
    def __init__(self, order_id: UUID) -> None:
        super().__init__(
            message=f"Заказ {order_id} не найден.",
            error_code=AppErrorCode.ORDER_NOT_FOUND,
        )
