from abc import ABC, abstractmethod
from uuid import UUID

from zernyshko.app.dtos.pagination import Pagination
from zernyshko.app.dtos.user import ResponseStaffUserDetailDTO, ResponseStaffUserListDTO


class UserReader(ABC):
    @abstractmethod
    async def get_list(self, pagination: Pagination) -> ResponseStaffUserListDTO:
        raise NotImplementedError()

    @abstractmethod
    async def get_detail(self, user_id: UUID) -> ResponseStaffUserDetailDTO | None:
        raise NotImplementedError()
