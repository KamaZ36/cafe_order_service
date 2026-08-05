from dataclasses import dataclass

from zernyshko.app.dtos.order import ResponseOrderListDTO
from zernyshko.app.dtos.pagination import Pagination
from zernyshko.infrastructure.identity_provider.base import IdentityProvider
from zernyshko.infrastructure.readers.order.base import OrderReader


@dataclass(frozen=True, eq=False)
class GetOrderListQuery:
    pagination: Pagination


class GetOrderListInteractor:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        order_reader: OrderReader,
    ) -> None:
        self._identity_provider = identity_provider
        self._order_reader = order_reader

    async def __call__(self, query: GetOrderListQuery) -> ResponseOrderListDTO:
        user_id = await self._identity_provider.get_current_user_id()

        return await self._order_reader.get_list_by_user_id(
            user_id=user_id, pagination=query.pagination
        )
