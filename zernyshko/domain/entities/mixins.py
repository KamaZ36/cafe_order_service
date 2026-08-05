from datetime import datetime

from zernyshko.utils import get_datetime_utc_now


class CreatedAtMixin:
    def __init__(self, created_at: datetime | None = None) -> None:
        self._created_at = (
            created_at if created_at is not None else get_datetime_utc_now()
        )

    @property
    def created_at(self) -> datetime:
        return self._created_at


class UpdatedAtMixin:
    def __init__(self, updated_at: datetime | None = None) -> None:
        self._updated_at = (
            updated_at if updated_at is not None else get_datetime_utc_now()
        )

    @property
    def updated_at(self) -> datetime:
        return self._updated_at
