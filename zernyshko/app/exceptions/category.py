from uuid import UUID

from zernyshko.app.exceptions.base import AppErrorCode, AppException


class CategoryNotFound(AppException):
    def __init__(self, category_id: UUID) -> None:
        super().__init__(
            message=f"Категория {category_id} не найдена.",
            error_code=AppErrorCode.CATEGORY_NOT_FOUND,
        )


class CategoryWithNameAlreadyExist(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Категория с таким именем уже существует.",
            error_code=AppErrorCode.CATEGORY_WITH_NAME_ALREADY_EXIST,
        )


class CategoryHasProducts(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="В категории есть товары — сначала перенеси или удали их.",
            error_code=AppErrorCode.CATEGORY_HAS_PRODUCTS,
        )
