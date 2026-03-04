from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.cart import ResponseCartDTO

from infrastructure.database.models.cart import CART_ITEM_TABLE, CART_TABLE
from infrastructure.database.models.product import PRODUCT_TABLE
from infrastructure.readers.cart.base import BaseCartReader


class SQLAlchemyCartReader(BaseCartReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_user_id(self, user_id: UUID) -> ResponseCartDTO | None:
        query = (
            select(
                CART_TABLE.c.id.label("cart_id"),
                CART_TABLE.c.user_id,
                CART_ITEM_TABLE.c.id.label("item_id"),
                CART_ITEM_TABLE.c.quantity,
                PRODUCT_TABLE.c.id.label("product_id"),
                PRODUCT_TABLE.c.name.label("product_name"),
                PRODUCT_TABLE.c.price,
                PRODUCT_TABLE.c.image,
                PRODUCT_TABLE.c.is_available,
                (PRODUCT_TABLE.c.price * CART_ITEM_TABLE.c.quantity).label(
                    "item_total"
                ),
            )
            .select_from(
                CART_TABLE.outerjoin(
                    CART_ITEM_TABLE, CART_TABLE.c.id == CART_ITEM_TABLE.c.cart_id
                ).outerjoin(
                    PRODUCT_TABLE, CART_ITEM_TABLE.c.product_id == PRODUCT_TABLE.c.id
                )
            )
            .where(CART_TABLE.c.user_id == user_id)
        )
        result = await self._session.execute(query)
        rows = result.fetchall()

        raise Exception(rows)
