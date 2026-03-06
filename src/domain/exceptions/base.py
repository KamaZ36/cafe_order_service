from enum import Enum


class DomainErrorCode(str, Enum):
    # КОРЗИНА

    PRODUCT_NOT_EXIST_IN_CART = "PRODUCT_NOT_EXIST_IN_CART"


class DomainException(Exception):
    def __init__(self, message: str, error_code: DomainErrorCode) -> None:
        super().__init__(message)
        self.error_code = error_code
