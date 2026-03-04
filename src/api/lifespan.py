from contextlib import asynccontextmanager
from typing import AsyncGenerator

from infrastructure.database.models import cart, category, product, user, session


@asynccontextmanager
async def lifespan(app) -> AsyncGenerator:
    yield
