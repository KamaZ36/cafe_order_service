from enum import Enum


class DomainErrorCode(str, Enum):
    # КОРЗИНА

    PRODUCT_NOT_EXIST_IN_CART = "PRODUCT_NOT_EXIST_IN_CART"

    # ЗАКАЗ

    INVALID_ORDER_STATUS_TRANSITION = "INVALID_ORDER_STATUS_TRANSITION"

    # ПЛАТЁЖ

    INVALID_PAYMENT_STATUS_TRANSITION = "INVALID_PAYMENT_STATUS_TRANSITION"


class DomainException(Exception):
    def __init__(self, message: str, error_code: DomainErrorCode) -> None:
        super().__init__(message)
        self.error_code = error_code
