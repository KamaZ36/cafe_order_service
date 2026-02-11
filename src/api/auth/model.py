from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import UUID

from src.utils import get_datetime_utc_now


@dataclass(eq=False)
class AuthSession:
    session_id: UUID
    user_id: UUID
    ip_address: str
    created_at: datetime
    expires_at: datetime

    @property
    def is_expired(self) -> bool:
        return datetime.now(tz=timezone.utc) > self.expires_at_dt

    @classmethod
    def create(
        cls, session_id: UUID, user_id: UUID, ip_address: str, ttl_hours: int = 720
    ) -> "AuthSession":
        now = get_datetime_utc_now()
        expires_at = now + timedelta(hours=ttl_hours)
        return cls(
            session_id=session_id,
            user_id=user_id,
            ip_address=ip_address,
            created_at=now,
            expires_at=expires_at,
        )
