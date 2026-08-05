from zernyshko.app.exceptions.base import AppErrorCode, AppException


class UnauthorizedError(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Пользователь не авторизован.",
            error_code=AppErrorCode.UNAUTHORIZED,
        )


class AccessDenied(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Недостаточно прав для выполнения действия.",
            error_code=AppErrorCode.ACCESS_DENIED,
        )


class AuthCodeNotValid(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Код подтверждения неверен или истёк.",
            error_code=AppErrorCode.AUTH_CODE_NOT_VALID,
        )


class RateLimitExceeded(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Слишком много попыток. Попробуйте позже.",
            error_code=AppErrorCode.RATE_LIMIT_EXCEEDED,
        )
