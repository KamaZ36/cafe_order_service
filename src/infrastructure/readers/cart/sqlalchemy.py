from decimal import Decimal
from uuid import UUID

from sqlalchemy import join, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos.cart import ResponseCartDTO, ResponseCartItemDTO

from infrastructure.database.models.cart import CART_ITEM_TABLE, CART_TABLE
from infrastructure.database.models.product import PRODUCT_TABLE
from infrastructure.readers.cart.base import BaseCartReader


class SQLAlchemyCartReader(BaseCartReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_user_id(self, user_id: UUID) -> ResponseCartDTO | None:
        query_cart = (
            select(CART_TABLE.c.id.label("cart_id"))
            .where(CART_TABLE.c.user_id == user_id)
            .limit(1)
        )

        result = await self._session.execute(query_cart)
        cart_id = result.scalar()

        query_cart_items = (
            select(
                CART_ITEM_TABLE.c.product_id,
                CART_ITEM_TABLE.c.quantity,
                PRODUCT_TABLE.c.name,
                PRODUCT_TABLE.c.image,
                PRODUCT_TABLE.c.price,
            )
            .select_from(join(CART_ITEM_TABLE, PRODUCT_TABLE))
            .where(CART_ITEM_TABLE.c.cart_id == cart_id)
        )

        result = await self._session.execute(query_cart_items)
        row_items = result.all()

        items = []
        total_price = Decimal("0")

        for row in row_items:
            item_total_price = row.price * row.quantity
            items.append(
                ResponseCartItemDTO(
                    product_id=row.product_id,
                    name=row.name,
                    image=row.image,
                    price=row.price,
                    quantity=row.quantity,
                    item_total_price=item_total_price,
                )
            )
            total_price += item_total_price

        return ResponseCartDTO(
            id=cart_id,
            total_items=len(row_items),
            total_price=total_price,
            items=tuple(items),
        )
