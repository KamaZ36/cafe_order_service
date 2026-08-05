from dataclasses import dataclass

from zernyshko.app.dtos.order import ResponseOrderListDTO
from zernyshko.app.dtos.pagination import Pagination
from zernyshko.app.exceptions.auth import AccessDenied
from zernyshko.domain.entities.order import OrderStatus
from zernyshko.infrastructure.identity_provider.base import IdentityProvider
from zernyshko.infrastructure.readers.order.base import OrderReader


@dataclass(frozen=True, eq=False)
class GetStaffOrderListQuery:
    pagination: Pagination
    status: OrderStatus | None = None


class GetStaffOrderListInteractor:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        order_reader: OrderReader,
    ) -> None:
        self._identity_provider = identity_provider
        self._order_reader = order_reader

    async def __call__(self, query: GetStaffOrderListQuery) -> ResponseOrderListDTO:
        current_user = await self._identity_provider.get_current_user()
        if not current_user.is_staff():
            raise AccessDenied()

        return await self._order_reader.get_list(
            pagination=query.pagination, status=query.status
        )
