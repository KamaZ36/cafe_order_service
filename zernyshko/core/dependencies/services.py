from typing import AsyncGenerator

import httpx
from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from zernyshko.api.auth.auth_service import AuthService
from zernyshko.app.services.cart import CartService
from zernyshko.app.services.product import ProductService
from zernyshko.core.config import settings
from zernyshko.infrastructure.database.transaction_manager.base import TransactionManager
from zernyshko.infrastructure.file_storage.base import BaseFileStorage
from zernyshko.infrastructure.payment.base import PaymentGateway
from zernyshko.infrastructure.payment.console import ConsolePaymentGateway
from zernyshko.infrastructure.payment.yookassa import YooKassaPaymentGateway
from zernyshko.infrastructure.repositories.cart.base import BaseCartRepository
from zernyshko.infrastructure.repositories.session.base import BaseSessionRepository
from zernyshko.infrastructure.security.password_hasher import PasswordHasher
from zernyshko.infrastructure.services.rate_limiter import RedisRateLimiter
from zernyshko.infrastructure.sms.base import SmsSender
from zernyshko.infrastructure.sms.console import ConsoleSmsSender
from zernyshko.infrastructure.sms.unconfigured import UnconfiguredSmsSender
from zernyshko.infrastructure.verification.base import PhoneVerificationCodeStorage
from zernyshko.infrastructure.verification.redis import RedisPhoneVerificationCodeStorage


class ServicesProvider(Provider):
    scope = Scope.REQUEST

    password_hasher = provide(PasswordHasher)

    @provide
    def get_rate_limiter(self, redis_client: Redis) -> RedisRateLimiter:
        return RedisRateLimiter(redis_client)

    @provide
    def get_phone_code_storage(self, redis_client: Redis) -> PhoneVerificationCodeStorage:
        return RedisPhoneVerificationCodeStorage(redis_client)

    @provide
    def get_sms_sender(self) -> SmsSender:
        if settings.debug:
            return ConsoleSmsSender()
        return UnconfiguredSmsSender()

    @provide
    def get_auth_service(
        self,
        auth_session_repository: BaseSessionRepository,
        transaction_manager: TransactionManager,
    ) -> AuthService:
        return AuthService(
            session_repository=auth_session_repository,
            transaction_manager=transaction_manager,
        )

    @provide
    def get_cart_service(self, cart_repository: BaseCartRepository) -> CartService:
        return CartService(cart_repository)

    @provide
    def get_product_service(self, file_storage: BaseFileStorage) -> ProductService:
        return ProductService(file_storage)

    @provide(scope=Scope.APP)
    async def get_yookassa_http_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        async with httpx.AsyncClient(
            base_url="https://api.yookassa.ru",
            auth=(settings.yookassa_shop_id, settings.yookassa_secret_key),
            timeout=10.0,
        ) as client:
            yield client

    @provide
    def get_payment_gateway(self, http_client: httpx.AsyncClient) -> PaymentGateway:
        if settings.debug:
            return ConsolePaymentGateway()
        return YooKassaPaymentGateway(http_client=http_client)
