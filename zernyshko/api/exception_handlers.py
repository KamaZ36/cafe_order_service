import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from zernyshko.app.exceptions.base import AppErrorCode, AppException
from zernyshko.domain.exceptions.base import DomainErrorCode, DomainException

logger = logging.getLogger("zernyshko.errors")

APP_ERROR_STATUS_CODES: dict[AppErrorCode, int] = {
    AppErrorCode.USER_ALREADY_EXIST: status.HTTP_409_CONFLICT,
    AppErrorCode.USER_NOT_FOUND: status.HTTP_404_NOT_FOUND,
    AppErrorCode.USER_PHONE_NUMBER_REQUIRED: status.HTTP_400_BAD_REQUEST,
    AppErrorCode.INVALID_CREDENTIALS: status.HTTP_401_UNAUTHORIZED,
    AppErrorCode.PRODUCT_NOT_FOUND: status.HTTP_404_NOT_FOUND,
    AppErrorCode.PRODUCT_IS_NOT_AVAILABLE: status.HTTP_409_CONFLICT,
    AppErrorCode.PRODUCT_IS_NOT_IN_CART: status.HTTP_404_NOT_FOUND,
    AppErrorCode.INCORRECT_PRODUCT_QUANTITY: status.HTTP_400_BAD_REQUEST,
    AppErrorCode.PRODUCT_WITH_NAME_ALREADY_EXIST: status.HTTP_409_CONFLICT,
    AppErrorCode.ORDER_NOT_FOUND: status.HTTP_404_NOT_FOUND,
    AppErrorCode.UNAUTHORIZED: status.HTTP_401_UNAUTHORIZED,
    AppErrorCode.ACCESS_DENIED: status.HTTP_403_FORBIDDEN,
    AppErrorCode.AUTH_CODE_NOT_VALID: status.HTTP_400_BAD_REQUEST,
    AppErrorCode.RATE_LIMIT_EXCEEDED: status.HTTP_429_TOO_MANY_REQUESTS,
}

DOMAIN_ERROR_STATUS_CODES: dict[DomainErrorCode, int] = {
    DomainErrorCode.PRODUCT_NOT_EXIST_IN_CART: status.HTTP_404_NOT_FOUND,
    DomainErrorCode.INVALID_ORDER_STATUS_TRANSITION: status.HTTP_409_CONFLICT,
}


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    status_code = APP_ERROR_STATUS_CODES.get(exc.error_code, status.HTTP_400_BAD_REQUEST)

    logger.warning(
        "%s %s -> %s: %s",
        request.method,
        request.url.path,
        exc.error_code.value,
        str(exc),
        extra={
            "http_method": request.method,
            "http_path": request.url.path,
            "error_code": exc.error_code.value,
        },
    )

    return JSONResponse(
        status_code=status_code,
        content={"error_code": exc.error_code.value, "message": str(exc)},
    )


async def domain_exception_handler(
    request: Request, exc: DomainException
) -> JSONResponse:
    status_code = DOMAIN_ERROR_STATUS_CODES.get(
        exc.error_code, status.HTTP_400_BAD_REQUEST
    )

    logger.warning(
        "%s %s -> %s: %s",
        request.method,
        request.url.path,
        exc.error_code.value,
        str(exc),
        extra={
            "http_method": request.method,
            "http_path": request.url.path,
            "error_code": exc.error_code.value,
        },
    )

    return JSONResponse(
        status_code=status_code,
        content={"error_code": exc.error_code.value, "message": str(exc)},
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        "Unhandled exception on %s %s: %s",
        request.method,
        request.url.path,
        exc,
        exc_info=exc,
        extra={
            "http_method": request.method,
            "http_path": request.url.path,
        },
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "Внутренняя ошибка сервера.",
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(DomainException, domain_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
