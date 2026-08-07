import os
import subprocess
from decimal import Decimal
from pathlib import Path
from typing import AsyncGenerator
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from testcontainers.community.postgres import PostgresContainer
from testcontainers.community.redis import RedisContainer

PROJECT_ROOT = Path(__file__).resolve().parent.parent

APP_TABLES = [
    "payments",
    "order_items",
    "orders",
    "cart_items",
    "carts",
    "sessions",
    "products",
    "categories",
    "users",
]

ADMIN_PHONE_NUMBER = "+70000000000"
ADMIN_PASSWORD = "password123"
MANAGER_PHONE_NUMBER = "+70000000099"
MANAGER_PASSWORD = "password123"


@pytest.fixture(scope="session", autouse=True)
def containers() -> None:
    with (
        PostgresContainer(
            "postgres:18.1",
            username="user",
            password="password",
            dbname="database",
            driver=None,
        ) as pg,
        RedisContainer("redis:7-alpine") as redis,
    ):
        os.environ["db_user"] = "user"
        os.environ["db_password"] = "password"
        os.environ["db_host"] = pg.get_container_host_ip()
        os.environ["db_port"] = str(pg.get_exposed_port(5432))
        os.environ["db_database"] = "database"
        os.environ["debug"] = "True"
        os.environ["staff_provision_secret"] = "test-secret"
        os.environ["yookassa_shop_id"] = "test-shop-id"
        os.environ["yookassa_secret_key"] = "test-secret-key"
        os.environ["frontend_base_url"] = "http://localhost:3000"
        os.environ["redis_host"] = redis.get_container_host_ip()
        os.environ["redis_port"] = str(redis.get_exposed_port(6379))

        subprocess.run(
            ["poetry", "run", "alembic", "upgrade", "head"],
            cwd=PROJECT_ROOT,
            env=os.environ.copy(),
            check=True,
            capture_output=True,
        )

        yield


@pytest.fixture(scope="session")
def app(containers: None):
    from zernyshko.api.main import create_app

    return create_app()


@pytest_asyncio.fixture(autouse=True)
async def clean_database(app) -> AsyncGenerator[None, None]:
    yield

    from sqlalchemy import text

    from zernyshko.infrastructure.database.connection import engine

    tables = ", ".join(APP_TABLES)
    async with engine.begin() as connection:
        await connection.execute(
            text(f"TRUNCATE TABLE {tables} RESTART IDENTITY CASCADE")
        )


@pytest_asyncio.fixture(autouse=True)
async def clean_redis(app) -> AsyncGenerator[None, None]:
    yield

    from redis.asyncio import Redis

    from zernyshko.core.config import settings

    redis_client = Redis.from_url(settings.redis_url)
    await redis_client.flushdb()
    await redis_client.aclose()


@pytest_asyncio.fixture
async def client(app) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def staff_client(app) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post(
            "/users/staff",
            json={"phone_number": ADMIN_PHONE_NUMBER, "password": ADMIN_PASSWORD},
            headers={"X-Staff-Secret": "test-secret"},
        )
        await client.post(
            "/users/login",
            json={"phone_number": ADMIN_PHONE_NUMBER, "password": ADMIN_PASSWORD},
        )
        yield client


@pytest_asyncio.fixture
async def manager_client(app) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post(
            "/users/staff",
            json={
                "phone_number": MANAGER_PHONE_NUMBER,
                "password": MANAGER_PASSWORD,
                "role": "MANAGER",
            },
            headers={"X-Staff-Secret": "test-secret"},
        )
        await client.post(
            "/users/login",
            json={"phone_number": MANAGER_PHONE_NUMBER, "password": MANAGER_PASSWORD},
        )
        yield client


@pytest_asyncio.fixture
async def category_id(staff_client: AsyncClient) -> str:
    response = await staff_client.post("/categories", json={"category_name": "Напитки"})
    return response.json()["id"]


@pytest_asyncio.fixture
async def product_id(app, category_id: str) -> str:
    from zernyshko.infrastructure.database.connection import async_session_maker
    from zernyshko.infrastructure.database.models.product import PRODUCT_TABLE

    new_id = uuid4()
    async with async_session_maker() as session:
        await session.execute(
            PRODUCT_TABLE.insert().values(
                id=new_id,
                name="Кофе",
                description="Черный кофе",
                weight="200мл",
                category_id=category_id,
                price=Decimal("150.00"),
                image=None,
                is_available=True,
                is_popular=False,
                is_new=False,
            )
        )
        await session.commit()

    return str(new_id)
