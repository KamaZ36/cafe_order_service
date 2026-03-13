from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class Pagination:
    limit: int = 0
    offset: int = 0
