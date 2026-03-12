from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class GetProductsQuery:
    limit: int
    offset: int


class GetProductsInteractor:
    def __init__(self) -> None:
        pass

    async def __call__(self):
        pass
