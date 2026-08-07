from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from zernyshko.domain.entities.user import UserRole


@dataclass(frozen=True, eq=False, kw_only=True)
class ResponseStaffUserForListDTO:
    id: UUID
    phone_number: str | None
    role: UserRole


@dataclass(frozen=True, eq=False, kw_only=True)
class ResponseStaffUserListDTO:
    total_count: int
    count: int
    users: list[ResponseStaffUserForListDTO]


@dataclass(frozen=True, eq=False, kw_only=True)
class ResponseUserSessionDTO:
    session_id: UUID
    ip_address: str | None
    created_at: datetime
    expires_at: datetime


@dataclass(frozen=True, eq=False, kw_only=True)
class ResponseStaffUserDetailDTO:
    id: UUID
    phone_number: str | None
    role: UserRole
    sessions: tuple[ResponseUserSessionDTO, ...]
