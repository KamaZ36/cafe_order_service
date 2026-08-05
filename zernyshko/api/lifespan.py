from contextlib import asynccontextmanager
from typing import AsyncGenerator

from zernyshko.infrastructure.database.models import (  # noqa: F401
    cart,
    category,
    order,
    product,
    session,
    user,
)


@asynccontextmanager
async def lifespan(app) -> AsyncGenerator:
    yield
