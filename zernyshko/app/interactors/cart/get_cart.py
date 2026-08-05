from decimal import Decimal

from zernyshko.app.dtos.cart import ResponseCartDTO
from zernyshko.infrastructure.identity_provider.base import IdentityProvider
from zernyshko.infrastructure.readers.cart.base import BaseCartReader


class GetCartInteractor:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        cart_reader: BaseCartReader,
    ) -> None:
        self._identity_provider = identity_provider
        self._cart_reader = cart_reader

    async def __call__(self) -> ResponseCartDTO:
        user_id = await self._identity_provider.get_current_user_id_or_none()
        if user_id is None:
            return ResponseCartDTO(
                id=None, total_items=0, total_price=Decimal("0"), items=()
            )

        return await self._cart_reader.get_by_user_id(user_id)
