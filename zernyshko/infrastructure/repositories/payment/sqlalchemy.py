from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from zernyshko.domain.entities.payment import Payment
from zernyshko.infrastructure.database.models.payment import PAYMENT_TABLE
from zernyshko.infrastructure.repositories.payment.base import PaymentRepository


class SQLAlchemyPaymentRepository(PaymentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, payment: Payment) -> None:
        self._session.add(payment)

    async def get_by_id(self, payment_id: UUID) -> Payment | None:
        payment = await self._session.get(Payment, payment_id)
        return payment if payment else None

    async def get_by_provider_payment_id(
        self, provider_payment_id: str
    ) -> Payment | None:
        query = select(Payment).where(
            PAYMENT_TABLE.c.provider_payment_id == provider_payment_id
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_order_id(self, order_id: UUID) -> Payment | None:
        query = (
            select(Payment)
            .where(PAYMENT_TABLE.c.order_id == order_id)
            .order_by(PAYMENT_TABLE.c.created_at.desc())
        )
        result = await self._session.execute(query)
        return result.scalars().first()
