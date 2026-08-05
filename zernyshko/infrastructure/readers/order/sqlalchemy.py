from uuid import UUID

from sqlalchemy import ColumnElement, func, join, select
from sqlalchemy.ext.asyncio import AsyncSession

from zernyshko.app.dtos.order import (
    ResponseOrderForListDTO,
    ResponseOrderItemDTO,
    ResponseOrderListDTO,
)
from zernyshko.app.dtos.pagination import Pagination
from zernyshko.domain.entities.order import OrderStatus
from zernyshko.infrastructure.database.models.order import ORDER_ITEM_TABLE, ORDER_TABLE
from zernyshko.infrastructure.database.models.product import PRODUCT_TABLE
from zernyshko.infrastructure.database.models.user import USER_TABLE
from zernyshko.infrastructure.readers.order.base import OrderReader


class SQLAlchemyOrderReader(OrderReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_list_by_user_id(
        self, user_id: UUID, pagination: Pagination
    ) -> ResponseOrderListDTO:
        return await self._fetch_orders(
            filters=[ORDER_TABLE.c.user_id == user_id],
            order_by=ORDER_TABLE.c.created_at.desc(),
            pagination=pagination,
        )

    async def get_list(
        self, pagination: Pagination, status: OrderStatus | None = None
    ) -> ResponseOrderListDTO:
        filters = [ORDER_TABLE.c.status == status] if status is not None else []
        return await self._fetch_orders(
            filters=filters,
            # Очередь для персонала — старые необработанные заказы первыми
            order_by=ORDER_TABLE.c.created_at.asc(),
            pagination=pagination,
        )

    async def _fetch_orders(
        self,
        filters: list[ColumnElement[bool]],
        order_by: ColumnElement,
        pagination: Pagination,
    ) -> ResponseOrderListDTO:
        count_query = select(func.count()).select_from(ORDER_TABLE).where(*filters)
        total_count = await self._session.scalar(count_query)

        orders_query = (
            select(ORDER_TABLE, USER_TABLE.c.phone_number)
            .select_from(
                join(ORDER_TABLE, USER_TABLE, ORDER_TABLE.c.user_id == USER_TABLE.c.id)
            )
            .where(*filters)
            .order_by(order_by)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        order_rows = (await self._session.execute(orders_query)).all()
        order_ids = [row.id for row in order_rows]

        items_by_order: dict[UUID, list[ResponseOrderItemDTO]] = {
            order_id: [] for order_id in order_ids
        }
        if order_ids:
            items_query = (
                select(
                    ORDER_ITEM_TABLE.c.order_id,
                    ORDER_ITEM_TABLE.c.product_id,
                    ORDER_ITEM_TABLE.c.quantity,
                    ORDER_ITEM_TABLE.c.price_at_order,
                    ORDER_ITEM_TABLE.c.item_total_price,
                    PRODUCT_TABLE.c.name,
                )
                .select_from(join(ORDER_ITEM_TABLE, PRODUCT_TABLE))
                .where(ORDER_ITEM_TABLE.c.order_id.in_(order_ids))
            )
            for row in (await self._session.execute(items_query)).all():
                items_by_order[row.order_id].append(
                    ResponseOrderItemDTO(
                        product_id=row.product_id,
                        name=row.name,
                        price_at_order=row.price_at_order,
                        item_total_price=row.item_total_price,
                        quantity=row.quantity,
                    )
                )

        orders = [
            ResponseOrderForListDTO(
                id=row.id,
                order_number=row.order_number,
                status=row.status,
                order_type=row.order_type,
                desired_time=row.desired_time,
                total_amount=row.total_amount,
                comment=row.comment,
                created_at=row.created_at,
                items=tuple(items_by_order[row.id]),
                customer_phone_number=row.phone_number,
                cancel_reason=row.cancel_reason,
            )
            for row in order_rows
        ]

        return ResponseOrderListDTO(
            total_count=total_count, count=len(orders), orders=orders
        )
