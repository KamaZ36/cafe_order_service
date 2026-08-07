from abc import ABC, abstractmethod
from uuid import UUID

from zernyshko.app.dtos.pagination import Pagination
from zernyshko.app.dtos.payment import ResponsePaymentListDTO


class PaymentReader(ABC):
    @abstractmethod
    async def get_list_by_user_id(
        self, user_id: UUID, pagination: Pagination
    ) -> ResponsePaymentListDTO:
        raise NotImplementedError()
