from zernyshko.domain.exceptions.base import DomainErrorCode, DomainException


class ProductNotExistInCart(DomainException):
    def __init__(self) -> None:
        super().__init__(
            message="Товар отсутствует в корзине",
            error_code=DomainErrorCode.PRODUCT_NOT_EXIST_IN_CART,
        )
