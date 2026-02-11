from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, eq=False)
class AuthenticatedCommand:
    user_id: UUID


@dataclass(frozen=True, eq=False)
class AuthenticatedQuery:
    user_id: UUID
