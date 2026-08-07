from uuid import UUID

from sqlalchemy import func, join, select
from sqlalchemy.ext.asyncio import AsyncSession

from zernyshko.app.dtos.pagination import Pagination
from zernyshko.app.dtos.payment import ResponsePaymentDTO, ResponsePaymentListDTO
from zernyshko.infrastructure.database.models.order import ORDER_TABLE
from zernyshko.infrastructure.database.models.payment import PAYMENT_TABLE
from zernyshko.infrastructure.readers.payment.base import PaymentReader


class SQLAlchemyPaymentReader(PaymentReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_list_by_user_id(
        self, user_id: UUID, pagination: Pagination
    ) -> ResponsePaymentListDTO:
        count_query = (
            select(func.count())
            .select_from(PAYMENT_TABLE)
            .where(PAYMENT_TABLE.c.user_id == user_id)
        )
        total_count = await self._session.scalar(count_query)

        query = (
            select(
                PAYMENT_TABLE.c.id,
                PAYMENT_TABLE.c.order_id,
                PAYMENT_TABLE.c.amount,
                PAYMENT_TABLE.c.status,
                PAYMENT_TABLE.c.created_at,
                ORDER_TABLE.c.order_number,
            )
            .select_from(
                join(
                    PAYMENT_TABLE,
                    ORDER_TABLE,
                    PAYMENT_TABLE.c.order_id == ORDER_TABLE.c.id,
                )
            )
            .where(PAYMENT_TABLE.c.user_id == user_id)
            .order_by(PAYMENT_TABLE.c.created_at.desc())
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        rows = (await self._session.execute(query)).all()

        payments = [
            ResponsePaymentDTO(
                id=row.id,
                order_id=row.order_id,
                order_number=row.order_number,
                amount=row.amount,
                status=row.status,
                created_at=row.created_at,
            )
            for row in rows
        ]

        return ResponsePaymentListDTO(
            total_count=total_count, count=len(payments), payments=payments
        )
