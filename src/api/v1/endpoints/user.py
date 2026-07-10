from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from api.auth.dependencies import CurrentUserID, CurrentUserIP
from api.v1.schemas.cart import UpdateCartItemSchema
from api.v1.schemas.order import CreatePickupOrderSchema
from app.dtos.cart import ResponseCartDTO

from app.interactors.cart.get_cart import GetCartQuery, GetCartInteractor
from app.interactors.cart.add_item_to_cart import (
    AddItemToCartCommand,
    AddItemToCartInetractor,
)
from app.interactors.cart.update_cart_item import (
    UpdateCartItemCommand,
    UpdateCartItemInteractor,
)
from app.interactors.order.create import CreateOrderCommand, CreateOrderInteractor
from app.interactors.user.create_user import CreateUserCommand, CreateUserInteractor

from api.auth.auth_service import AuthService
from api.v1.schemas.user import AddItemToCartSchema, CreateUserSchema
from core.dependencies.container import container


router = APIRouter()


@router.post("")
async def create_user(
    data: CreateUserSchema, ip_address: CurrentUserIP
) -> JSONResponse:
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
    "/@me/cart", description="Получить корзину текущего, авторизованного пользователя."
)
async def get_cart_current_user(user_id: CurrentUserID) -> ResponseCartDTO:
    query = GetCartQuery(user_id=user_id)
    async with container() as context:
        interactor = await context.get(GetCartInteractor)
        cart = await interactor(query)
    return cart


@router.post(
    "/@me/cart/items", description="Добавить товар в корзину текущего пользователя."
)
async def add_item_to_cart_current_user(
    user_id: CurrentUserID, data: AddItemToCartSchema
) -> None:

    response = JSONResponse(content={"result": "OK!"})

    if user_id is None:
        command = CreateUserCommand()
        async with container() as context:
            interactor = await context.get(CreateUserInteractor)
            auth_service = await context.get(AuthService)

            user_id = await interactor(command)
            auth_session = await auth_service.create_user_session(user_id=user_id)

        response.set_cookie(
            key="session_id", value=auth_session.session_id, httponly=True
        )

    command = AddItemToCartCommand(
        user_id=user_id, product_id=data.product_id, quantity=data.quantity
    )
    async with container() as context:
        interactor = await context.get(AddItemToCartInetractor)
        await interactor(command)

    return response


@router.patch(
    "/@me/cart/items/{product_id}/quantity",
    description="Изменить количество товара в корзине",
)
async def update_cart_item_quantity(
    product_id: UUID, data: UpdateCartItemSchema, user_id: CurrentUserID
) -> None:
    command = UpdateCartItemCommand(
        user_id=user_id, product_id=product_id, quantity=data.quantity
    )
    async with container() as context:
        interactor = await context.get(UpdateCartItemInteractor)
        await interactor(command)


@router.post(
    "/@me/orders/pickup",
    description="Оформить заказ из активной корзины для текущего пользователя",
)
async def create_order_from_cart(
    user_id: CurrentUserID, data: CreatePickupOrderSchema
) -> None:
    command = CreateOrderCommand(
        user_id=user_id, desired_time=data.desired_time, comment=data.comment
    )
    async with container() as context:
        interactor = await context.get(CreateOrderInteractor)
        await interactor(command)
