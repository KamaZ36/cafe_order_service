from dataclasses import dataclass
from uuid import UUID

from zernyshko.app.dtos.pagination import Pagination
from zernyshko.app.dtos.payment import ResponsePaymentListDTO
from zernyshko.app.exceptions.auth import AccessDenied
from zernyshko.infrastructure.identity_provider.base import IdentityProvider
from zernyshko.infrastructure.readers.payment.base import PaymentReader


@dataclass(frozen=True, eq=False)
class GetStaffUserPaymentsQuery:
    user_id: UUID
    pagination: Pagination


class GetStaffUserPaymentsInteractor:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        payment_reader: PaymentReader,
    ) -> None:
        self._identity_provider = identity_provider
        self._payment_reader = payment_reader

    async def __call__(
        self, query: GetStaffUserPaymentsQuery
    ) -> ResponsePaymentListDTO:
        current_user = await self._identity_provider.get_current_user()
        if not current_user.is_admin():
            raise AccessDenied()

        return await self._payment_reader.get_list_by_user_id(
            user_id=query.user_id, pagination=query.pagination
        )
