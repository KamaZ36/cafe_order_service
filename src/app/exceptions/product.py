from uuid import UUID

from src.app.exceptions.base import AppErrorCode, AppException


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


class ProductIsNotInCart(AppException):
    def __init__(self, cart_item_id: UUID) -> None:
        super().__init__(
            message=f"Товар {cart_item_id} не находится в корзине.",
            error_code=AppErrorCode.PRODUCT_IS_NOT_IN_CART,
        )


class IncorretQuantityValue(AppException):
    def __init__(self) -> None:
        super().__init(
            message="Количество продукта слишком большое.",
            error_code=AppErrorCode.INCORRECT_PRODUCT_QUANTITY,
        )


class ProductWithNameAlreadyExist(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Товар с таким именем уже существует.",
            error_code=AppErrorCode.PRODUCT_WITH_NAME_ALREADY_EXIST,
        )
