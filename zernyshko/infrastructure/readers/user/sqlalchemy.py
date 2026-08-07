from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from zernyshko.app.dtos.pagination import Pagination
from zernyshko.app.dtos.user import (
    ResponseStaffUserDetailDTO,
    ResponseStaffUserForListDTO,
    ResponseStaffUserListDTO,
    ResponseUserSessionDTO,
)
from zernyshko.infrastructure.database.models.session import AUTH_SESSION_TABLE
from zernyshko.infrastructure.database.models.user import USER_TABLE
from zernyshko.infrastructure.readers.user.base import UserReader


class SQLAlchemyUserReader(UserReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_list(self, pagination: Pagination) -> ResponseStaffUserListDTO:
        total_count = await self._session.scalar(
            select(func.count()).select_from(USER_TABLE)
        )

        query = (
            select(USER_TABLE)
            # id — uuid7, он же хронологический порядок: новые пользователи первыми
            .order_by(USER_TABLE.c.id.desc())
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        rows = (await self._session.execute(query)).all()

        users = [
            ResponseStaffUserForListDTO(
                id=row.id, phone_number=row.phone_number, role=row.role
            )
            for row in rows
        ]

        return ResponseStaffUserListDTO(
            total_count=total_count, count=len(users), users=users
        )

    async def get_detail(self, user_id: UUID) -> ResponseStaffUserDetailDTO | None:
        user_row = (
            await self._session.execute(
                select(USER_TABLE).where(USER_TABLE.c.id == user_id)
            )
        ).first()
        if user_row is None:
            return None

        sessions_query = (
            select(AUTH_SESSION_TABLE)
            .where(AUTH_SESSION_TABLE.c.user_id == user_id)
            .order_by(AUTH_SESSION_TABLE.c.created_at.desc())
        )
        sessions = tuple(
            ResponseUserSessionDTO(
                session_id=row.session_id,
                ip_address=row.ip_address,
                created_at=row.created_at,
                expires_at=row.expires_at,
            )
            for row in (await self._session.execute(sessions_query)).all()
        )

        return ResponseStaffUserDetailDTO(
            id=user_row.id,
            phone_number=user_row.phone_number,
            role=user_row.role,
            sessions=sessions,
        )
