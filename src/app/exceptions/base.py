from enum import Enum


class AppErrorCode(str, Enum):
    # Пользователи
    USER_ALREADY_EXIST = "USER_ALREADY_EXIST"

    # Продукты
    PRODUCT_NOT_FOUND = "PRODUCT_NOT_FOUND"
    PRODUCT_IS_NOT_AVAILABLE = "PRODUCT_IS_NOT_AVAILABLE"
    PRODUCT_IS_NOT_IN_CART = "PRODUCT_IS_NOT_IN_CART"
    INCORRECT_PRODUCT_QUANTITY = "INCORRECT_PRODUCT_QUANTITY"


class AppException(Exception):
    def __init__(self, message: str, error_code: AppErrorCode) -> None:
        super().__init__(message)
        self.error_code = error_code
