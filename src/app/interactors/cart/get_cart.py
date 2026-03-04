from dataclasses import dataclass

from app.dtos.cart import ResponseCartDTO
from app.interactors.common import AuthenticatedCommand

from infrastructure.readers.cart.base import BaseCartReader


@dataclass(frozen=True, eq=False)
class GetCartQuery(AuthenticatedCommand):
    pass


class GetOrCreateCartInteractor:
    def __init__(
        self,
        cart_reader: BaseCartReader,
    ) -> None:
        self._cart_reader = cart_reader

    async def __call__(self, query: GetCartQuery) -> ResponseCartDTO | None:
        await self._cart_reader.get_by_user_id(query.user_id)
