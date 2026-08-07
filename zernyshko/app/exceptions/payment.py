from uuid import UUID

from zernyshko.app.exceptions.base import AppErrorCode, AppException


class PaymentNotFound(AppException):
    def __init__(self, provider_payment_id: str) -> None:
        super().__init__(
            message=f"Платёж {provider_payment_id} не найден.",
            error_code=AppErrorCode.PAYMENT_NOT_FOUND,
        )


class PaymentNotFoundForOrder(AppException):
    def __init__(self, order_id: UUID) -> None:
        super().__init__(
            message=f"Платёж для заказа {order_id} не найден.",
            error_code=AppErrorCode.PAYMENT_NOT_FOUND,
        )
