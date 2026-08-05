from uuid import UUID

from fastapi import APIRouter, Query, Request

from zernyshko.api.v1.schemas.order import GetStaffOrderListSchema, StaffCancelOrderSchema
from zernyshko.app.dtos.order import ResponseOrderListDTO
from zernyshko.app.dtos.pagination import Pagination
from zernyshko.app.interactors.order.cancel import (
    StaffCancelOrderCommand,
    StaffCancelOrderInteractor,
)
from zernyshko.app.interactors.order.complete import (
    CompleteOrderCommand,
    CompleteOrderInteractor,
)
from zernyshko.app.interactors.order.confirm import (
    ConfirmOrderCommand,
    ConfirmOrderInteractor,
)
from zernyshko.app.interactors.order.get_orders import (
    GetStaffOrderListInteractor,
    GetStaffOrderListQuery,
)
from zernyshko.app.interactors.order.mark_ready import (
    MarkOrderReadyCommand,
    MarkOrderReadyInteractor,
)
from zernyshko.core.dependencies.container import container

router = APIRouter()


@router.get(
    "",
    description="Список всех заказов для персонала кафе (очередь).",
)
async def get_staff_order_list(
    request: Request, data: GetStaffOrderListSchema = Query(...)
) -> ResponseOrderListDTO:
    query = GetStaffOrderListQuery(
        pagination=Pagination(limit=data.limit, offset=data.offset),
        status=data.status,
    )
    async with container(context={Request: request}) as context:
        interactor = await context.get(GetStaffOrderListInteractor)
        return await interactor(query)


@router.patch(
    "/{order_id}/confirm",
    description="Подтвердить заказ (персонал кафе).",
)
async def confirm_order(order_id: UUID, request: Request) -> None:
    command = ConfirmOrderCommand(order_id=order_id)
    async with container(context={Request: request}) as context:
        interactor = await context.get(ConfirmOrderInteractor)
        await interactor(command)


@router.patch(
    "/{order_id}/ready",
    description="Отметить заказ готовым к выдаче (персонал кафе).",
)
async def mark_order_ready(order_id: UUID, request: Request) -> None:
    command = MarkOrderReadyCommand(order_id=order_id)
    async with container(context={Request: request}) as context:
        interactor = await context.get(MarkOrderReadyInteractor)
        await interactor(command)


@router.patch(
    "/{order_id}/complete",
    description="Отметить заказ выданным/завершённым (персонал кафе).",
)
async def complete_order(order_id: UUID, request: Request) -> None:
    command = CompleteOrderCommand(order_id=order_id)
    async with container(context={Request: request}) as context:
        interactor = await context.get(CompleteOrderInteractor)
        await interactor(command)


@router.patch(
    "/{order_id}/cancel",
    description="Отменить заказ (персонал кафе, доступно из любого активного статуса).",
)
async def staff_cancel_order(
    order_id: UUID, request: Request, data: StaffCancelOrderSchema = StaffCancelOrderSchema()
) -> None:
    command = StaffCancelOrderCommand(order_id=order_id, reason=data.reason)
    async with container(context={Request: request}) as context:
        interactor = await context.get(StaffCancelOrderInteractor)
        await interactor(command)
