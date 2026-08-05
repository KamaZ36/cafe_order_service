from uuid import UUID

from zernyshko.app.exceptions.base import AppErrorCode, AppException


class UserAlreadyExist(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Пользователь уже существует.",
            error_code=AppErrorCode.USER_ALREADY_EXIST,
        )


class UserNotFound(AppException):
    def __init__(self, user_id: UUID) -> None:
        super().__init__(
            message=f"Пользователь {user_id} не найден.",
            error_code=AppErrorCode.USER_NOT_FOUND,
        )


class UserPhoneNumberRequired(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Для оформления заказа укажите номер телефона.",
            error_code=AppErrorCode.USER_PHONE_NUMBER_REQUIRED,
        )


class InvalidCredentials(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Неверный номер телефона или пароль.",
            error_code=AppErrorCode.INVALID_CREDENTIALS,
        )
