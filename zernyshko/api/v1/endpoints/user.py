from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Header, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse

from zernyshko.api.auth.auth_service import AuthService
from zernyshko.api.auth.dependencies import CurrentUserIP
from zernyshko.api.v1.schemas.cart import UpdateCartItemSchema
from zernyshko.api.v1.schemas.order import CreatePickupOrderSchema, GetOrderListSchema
from zernyshko.api.v1.schemas.user import (
    AddItemToCartSchema,
    CreateUserSchema,
    CurrentUserResponseSchema,
    LoginSchema,
    PhoneLoginSchema,
    ProvisionStaffSchema,
    SendPhoneCodeSchema,
)
from zernyshko.app.dtos.cart import ResponseCartDTO
from zernyshko.app.dtos.order import ResponseOrderListDTO
from zernyshko.app.dtos.pagination import Pagination
from zernyshko.app.exceptions.auth import RateLimitExceeded
from zernyshko.app.interactors.cart.add_item_to_cart import (
    AddItemToCartCommand,
    AddItemToCartInetractor,
)
from zernyshko.app.interactors.cart.get_cart import GetCartInteractor
from zernyshko.app.interactors.cart.update_cart_item import (
    UpdateCartItemCommand,
    UpdateCartItemInteractor,
)
from zernyshko.app.interactors.order.create import (
    CreateOrderCommand,
    CreateOrderInteractor,
)
from zernyshko.app.interactors.user.cancel_order import (
    CancelOrderCommand,
    CancelOrderInteractor,
)
from zernyshko.app.interactors.user.create_user import (
    CreateUserCommand,
    CreateUserInteractor,
)
from zernyshko.app.interactors.user.get_current_user import GetCurrentUserInteractor
from zernyshko.app.interactors.user.get_orders import (
    GetOrderListInteractor,
    GetOrderListQuery,
)
from zernyshko.app.interactors.user.login import LoginCommand, LoginInteractor
from zernyshko.app.interactors.user.logout import LogoutInteractor
from zernyshko.app.interactors.user.provision_staff import (
    ProvisionStaffCommand,
    ProvisionStaffInteractor,
)
from zernyshko.app.interactors.user.resolve_phone_user import (
    ResolvePhoneUserCommand,
    ResolvePhoneUserInteractor,
)
from zernyshko.app.interactors.user.send_phone_code import (
    SendPhoneVerificationCodeCommand,
    SendPhoneVerificationCodeInteractor,
)
from zernyshko.app.interactors.user.verify_phone_code import (
    VerifyPhoneCodeCommand,
    VerifyPhoneCodeInteractor,
)
from zernyshko.core.config import settings
from zernyshko.core.dependencies.container import container
from zernyshko.infrastructure.identity_provider.base import IdentityProvider
from zernyshko.infrastructure.services.rate_limiter import RedisRateLimiter

router = APIRouter()


@router.post("")
async def create_user(data: CreateUserSchema, ip_address: CurrentUserIP) -> JSONResponse:
    command = CreateUserCommand(phone_number=data.phone_number)
    async with container() as context:
        interactor = await context.get(CreateUserInteractor)
        auth_service = await context.get(AuthService)

        user_id = await interactor(command)
        auth_session = await auth_service.create_user_session(
            user_id=user_id, ip_address=ip_address
        )

    response = JSONResponse(content={"user_id": str(user_id)})
    response.set_cookie(key="session_id", value=auth_session.session_id, httponly=True)

    return response


@router.get(
    "/@me",
    description="Данные текущего авторизованного пользователя. 401, если сессии нет.",
)
async def get_current_user(request: Request) -> CurrentUserResponseSchema:
    async with container(context={Request: request}) as context:
        interactor = await context.get(GetCurrentUserInteractor)
        user = await interactor()
    return CurrentUserResponseSchema.model_validate(user)


@router.post(
    "/phone/code",
    description=(
        "Отправить код подтверждения на номер телефона. Код действителен 10 минут."
    ),
)
async def send_phone_verification_code(
    data: SendPhoneCodeSchema, ip_address: CurrentUserIP
) -> JSONResponse:
    async with container() as context:
        limiter = await context.get(RedisRateLimiter)

        allowed_by_cooldown = await limiter.hit(
            f"rl:send_phone_code:cooldown:{data.phone_number}", limit=1, window_seconds=60
        )
        allowed_by_phone = await limiter.hit(
            f"rl:send_phone_code:phone:{data.phone_number}", limit=3, window_seconds=3600
        )
        allowed_by_ip = await limiter.hit(
            f"rl:send_phone_code:ip:{ip_address}", limit=10, window_seconds=3600
        )

        if not (allowed_by_cooldown and allowed_by_phone and allowed_by_ip):
            raise RateLimitExceeded()

        interactor = await context.get(SendPhoneVerificationCodeInteractor)
        await interactor(SendPhoneVerificationCodeCommand(phone_number=data.phone_number))

    return JSONResponse(content={"result": "OK!"})


@router.post(
    "/phone/login",
    description=(
        "Подтвердить телефон кодом из SMS (см. /users/phone/code) и войти. "
        "Если телефон уже принадлежит существующему аккаунту — вход в него "
        "(новая сессия). Если нет — телефон привязывается к текущей сессии "
        "(в т.ч. анонимной, созданной при добавлении товара в корзину) либо "
        "создаётся новый аккаунт, если сессии не было вовсе."
    ),
)
async def phone_login(
    request: Request, ip_address: CurrentUserIP, data: PhoneLoginSchema
) -> JSONResponse:
    async with container(context={Request: request}) as context:
        limiter = await context.get(RedisRateLimiter)

        allowed_by_phone = await limiter.hit(
            f"rl:verify_phone_code:phone:{data.phone_number}", limit=5, window_seconds=600
        )
        allowed_by_ip = await limiter.hit(
            f"rl:verify_phone_code:ip:{ip_address}", limit=20, window_seconds=3600
        )
        if not (allowed_by_phone and allowed_by_ip):
            raise RateLimitExceeded()

        verify_interactor = await context.get(VerifyPhoneCodeInteractor)
        await verify_interactor(
            VerifyPhoneCodeCommand(phone_number=data.phone_number, code=data.code)
        )

        identity_provider = await context.get(IdentityProvider)
        previous_user_id = await identity_provider.get_current_user_id_or_none()

        resolve_interactor = await context.get(ResolvePhoneUserInteractor)
        user_id = await resolve_interactor(
            ResolvePhoneUserCommand(phone_number=data.phone_number)
        )

        response = JSONResponse(content={"user_id": str(user_id)})

        if user_id != previous_user_id:
            auth_service = await context.get(AuthService)
            auth_session = await auth_service.create_user_session(
                user_id=user_id, ip_address=ip_address
            )
            response.set_cookie(
                key="session_id", value=auth_session.session_id, httponly=True
            )

    return response


@router.get(
    "/@me/cart", description="Получить корзину текущего, авторизованного пользователя."
)
async def get_cart_current_user(request: Request) -> ResponseCartDTO:
    async with container(context={Request: request}) as context:
        interactor = await context.get(GetCartInteractor)
        cart = await interactor()
    return cart


@router.post(
    "/@me/cart/items", description="Добавить товар в корзину текущего пользователя."
)
async def add_item_to_cart_current_user(
    request: Request, data: AddItemToCartSchema
) -> None:
    response = JSONResponse(content={"result": "OK!"})

    async with container(context={Request: request}) as context:
        identity_provider = await context.get(IdentityProvider)
        user_id = await identity_provider.get_current_user_id_or_none()

        if user_id is None:
            interactor = await context.get(CreateUserInteractor)
            auth_service = await context.get(AuthService)

            user_id = await interactor(CreateUserCommand())
            auth_session = await auth_service.create_user_session(user_id=user_id)

            response.set_cookie(
                key="session_id", value=auth_session.session_id, httponly=True
            )

        command = AddItemToCartCommand(
            user_id=user_id, product_id=data.product_id, quantity=data.quantity
        )
        interactor = await context.get(AddItemToCartInetractor)
        await interactor(command)

    return response


@router.patch(
    "/@me/cart/items/{product_id}/quantity",
    description="Изменить количество товара в корзине",
)
async def update_cart_item_quantity(
    product_id: UUID, data: UpdateCartItemSchema, request: Request
) -> None:
    command = UpdateCartItemCommand(product_id=product_id, quantity=data.quantity)
    async with container(context={Request: request}) as context:
        interactor = await context.get(UpdateCartItemInteractor)
        await interactor(command)


@router.get(
    "/@me/orders",
    description="История заказов текущего авторизованного пользователя.",
)
async def get_own_orders(
    request: Request, data: GetOrderListSchema = Query(...)
) -> ResponseOrderListDTO:
    query = GetOrderListQuery(pagination=Pagination(limit=data.limit, offset=data.offset))
    async with container(context={Request: request}) as context:
        interactor = await context.get(GetOrderListInteractor)
        return await interactor(query)


@router.post(
    "/@me/orders/pickup",
    description="Оформить заказ из активной корзины для текущего пользователя",
)
async def create_order_from_cart(request: Request, data: CreatePickupOrderSchema) -> None:
    command = CreateOrderCommand(desired_time=data.desired_time, comment=data.comment)
    async with container(context={Request: request}) as context:
        interactor = await context.get(CreateOrderInteractor)
        await interactor(command)


@router.patch(
    "/@me/orders/{order_id}/cancel",
    description=(
        "Отменить свой заказ. Доступно только пока заказ ещё не подтверждён кафе "
        "(статус PENDING)."
    ),
)
async def cancel_own_order(order_id: UUID, request: Request) -> None:
    command = CancelOrderCommand(order_id=order_id)
    async with container(context={Request: request}) as context:
        interactor = await context.get(CancelOrderInteractor)
        await interactor(command)


@router.post(
    "/login",
    description="Вход по номеру телефона и паролю. Используется персоналом кафе.",
)
async def login(data: LoginSchema, ip_address: CurrentUserIP) -> JSONResponse:
    command = LoginCommand(phone_number=data.phone_number, password=data.password)
    async with container() as context:
        interactor = await context.get(LoginInteractor)
        auth_service = await context.get(AuthService)

        user_id = await interactor(command)
        auth_session = await auth_service.create_user_session(
            user_id=user_id, ip_address=ip_address
        )

    response = JSONResponse(content={"user_id": str(user_id)})
    response.set_cookie(key="session_id", value=auth_session.session_id, httponly=True)

    return response


@router.post(
    "/logout",
    description="Выйти из текущей сессии.",
)
async def logout(request: Request) -> JSONResponse:
    async with container(context={Request: request}) as context:
        interactor = await context.get(LogoutInteractor)
        await interactor()

    response = JSONResponse(content={"result": "OK!"})
    response.delete_cookie("session_id")

    return response


@router.post(
    "/staff",
    description=(
        "Создать или повысить пользователя до роли ADMIN/MANAGER. Требует "
        "заголовок X-Staff-Secret с секретом из конфигурации сервера. "
        "Временная мера, пока в проекте нет полноценной админки для найма."
    ),
)
async def provision_staff(
    data: ProvisionStaffSchema,
    x_staff_secret: Annotated[str | None, Header()] = None,
) -> JSONResponse:
    if x_staff_secret != settings.staff_provision_secret:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    command = ProvisionStaffCommand(
        phone_number=data.phone_number, password=data.password, role=data.role
    )
    async with container() as context:
        interactor = await context.get(ProvisionStaffInteractor)
        user_id = await interactor(command)

    return JSONResponse(content={"user_id": str(user_id)})
