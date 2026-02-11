from dataclasses import dataclass
from uuid import UUID

from src.app.interactors.common import AuthenticatedCommand


@dataclass(frozen=True, eq=False)
class CreateOrderCommand(AuthenticatedCommand):
    cart_id: UUID


class CreateOrderInteractor:
    def __init__(self) -> None:
        pass
