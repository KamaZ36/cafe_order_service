from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from api.auth.dependencies import CurrentUserID, CurrentUserIP
from api.v1.schemas.cart import UpdateCartItemSchema
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
    command = AddItemToCartCommand(
        user_id=user_id, product_id=data.product_id, quantity=data.quantity
    )
    async with container() as context:
        interactor = await context.get(AddItemToCartInetractor)
        await interactor(command)


@router.patch(
    "/@me/cart/items/{product_id}", description="Изменить количество товара в корзине"
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


@router.get("/{user_id}/cart", description="Получить корзину пользователя.")
async def get_cart_user_by_id(user_id: UUID) -> ResponseCartDTO:
    query = GetCartQuery(user_id=user_id)
    async with container() as context:
        interactor = await context.get(GetCartInteractor)
        cart = await interactor(query)
    return cart


@router.post(
    "/{user_id}/cart/item", description="Добавить товар пользователю в корзину."
)
async def add_item_in_cart(user_id: UUID, data: AddItemToCartSchema) -> None:
    command = AddItemToCartCommand(
        user_id=user_id, product_id=data.product_id, quantity=data.quantity
    )
    async with container() as context:
        interactor = await context.get(AddItemToCartInetractor)
        await interactor(command)
