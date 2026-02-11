from dataclasses import dataclass
from uuid import UUID


@dataclass(kw_only=True)
class Category:
    id: UUID
    name: str
