from app.exceptions.base import AppErrorCode, AppException


class UserAlreadyExist(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Пользователь уже существует.",
            error_code=AppErrorCode.USER_ALREADY_EXIST,
        )
