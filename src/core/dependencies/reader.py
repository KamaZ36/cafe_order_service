from dishka import provide, Provider, Scope

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.readers.cart.base import BaseCartReader
from infrastructure.readers.cart.sqlalchemy import SQLAlchemyCartReader
from infrastructure.readers.product.base import ProductReader
from infrastructure.readers.product.sqlalchemy import SQLAlchemyProductReader


class ReaderProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_cart_reader(self, session: AsyncSession) -> BaseCartReader:
        return SQLAlchemyCartReader(session)

    @provide
    def get_product_reader(self, session: AsyncSession) -> ProductReader:
        return SQLAlchemyProductReader(session)
