from dishka import provide, Provider, Scope

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.readers.cart.base import BaseCartReader
from infrastructure.readers.cart.sqlalchemy import SQLAlchemyCartReader


class ReaderProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_cart_reader(self, session: AsyncSession) -> BaseCartReader:
        return SQLAlchemyCartReader(session)
