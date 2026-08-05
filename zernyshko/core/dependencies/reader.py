from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from zernyshko.infrastructure.readers.cart.base import BaseCartReader
from zernyshko.infrastructure.readers.cart.sqlalchemy import SQLAlchemyCartReader
from zernyshko.infrastructure.readers.order.base import OrderReader
from zernyshko.infrastructure.readers.order.sqlalchemy import SQLAlchemyOrderReader
from zernyshko.infrastructure.readers.product.base import ProductReader
from zernyshko.infrastructure.readers.product.sqlalchemy import SQLAlchemyProductReader


class ReaderProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_cart_reader(self, session: AsyncSession) -> BaseCartReader:
        return SQLAlchemyCartReader(session)

    @provide
    def get_product_reader(self, session: AsyncSession) -> ProductReader:
        return SQLAlchemyProductReader(session)

    @provide
    def get_order_reader(self, session: AsyncSession) -> OrderReader:
        return SQLAlchemyOrderReader(session)
