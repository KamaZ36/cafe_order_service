from dataclasses import dataclass, field
from datetime import datetime

from utils import get_datetime_utc_now


@dataclass
class CreatedAtMixin:
    created_at: datetime = field(default_factory=get_datetime_utc_now)


@dataclass
class UpdatedAtMixin:
    updated_at: datetime = field(default_factory=get_datetime_utc_now)
