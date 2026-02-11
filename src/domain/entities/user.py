from dataclasses import dataclass
from uuid import UUID


@dataclass(kw_only=True)
class User:
    id: UUID
    phone_number: str
