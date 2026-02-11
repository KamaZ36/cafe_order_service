from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.api.auth.dependencies import CurrentUserID, CurrentUserIP
from src.app.dtos.cart import ResponseCartDTO

from src.app.interactors.cart.get_cart import GetCartQuery, GetOrCreateCartInteractor
from src.app.interactors.cart.add_item_to_cart import (
    AddItemToCartCommand,
    AddItemToCartInetractor,
)
from src.app.interactors.user.create_user import CreateUserCommand, CreateUserInteractor

from src.api.auth.auth_service import AuthService
from src.api.v1.schemas.user import AddItemToCartSchema, CreateUserSchema
from src.core.dependencies.container import container


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
        interactor = await context.get(GetOrCreateCartInteractor)
        cart = await interactor(query)
    return cart


@router.post(
    "/@me/cart/item", description="Добавить товар в корзину текущего пользователя."
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


@router.get("/{user_id}/cart", description="Получить корзину пользователя.")
async def get_cart_user_by_id(user_id: UUID) -> ResponseCartDTO:
    query = GetCartQuery(user_id=user_id)
    async with container() as context:
        interactor = await context.get(GetOrCreateCartInteractor)
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
