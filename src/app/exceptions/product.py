from uuid import UUID
from app.exceptions.base import AppErrorCode, AppException


class ProductNotFound(AppException):
    def __init__(self, product_id: UUID) -> None:
        super().__init__(
            message=f"Продукт {product_id} не найден.",
            error_code=AppErrorCode.PRODUCT_NOT_FOUND,
        )


class ProductIsNotAvailable(AppException):
    def __init__(self, product_name: str) -> None:
        super().__init__(
            message=f"Продукт '{product_name}' сейчас недоступен или закончился.",
            error_code=AppErrorCode.PRODUCT_IS_NOT_AVAILABLE,
        )
