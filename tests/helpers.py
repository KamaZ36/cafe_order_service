async def get_latest_order_id(status: str | None = None) -> str:
    from sqlalchemy import select

    from zernyshko.infrastructure.database.connection import async_session_maker
    from zernyshko.infrastructure.database.models.order import ORDER_TABLE

    query = select(ORDER_TABLE.c.id).order_by(ORDER_TABLE.c.created_at.desc()).limit(1)
    if status is not None:
        query = query.where(ORDER_TABLE.c.status == status)

    async with async_session_maker() as session:
        result = await session.execute(query)
        return str(result.scalar_one())


async def pay_latest_order(client) -> None:
    """Симулирует успешную оплату последнего оформленного заказа — дёргает
    вебхук так же, как это сделала бы ЮKassa после списания денег."""
    from sqlalchemy import select

    from zernyshko.infrastructure.database.connection import async_session_maker
    from zernyshko.infrastructure.database.models.payment import PAYMENT_TABLE

    query = (
        select(PAYMENT_TABLE.c.provider_payment_id)
        .order_by(PAYMENT_TABLE.c.created_at.desc())
        .limit(1)
    )
    async with async_session_maker() as session:
        result = await session.execute(query)
        provider_payment_id = result.scalar_one()

    response = await client.post(
        "/payments/yookassa/webhook",
        json={"object": {"id": provider_payment_id}},
    )
    response.raise_for_status()


async def set_phone_number(client, phone_number: str) -> None:
    """Проходит цепочку отправки/подтверждения кода и привязывает телефон
    к текущей сессии клиента — тестовый хелпер, чтобы не дублировать эти
    два шага в каждом тесте, которому просто нужен привязанный телефон."""

    await client.post("/users/phone/code", json={"phone_number": phone_number})
    code = await get_phone_verification_code(phone_number)
    response = await client.post(
        "/users/phone/login", json={"phone_number": phone_number, "code": code}
    )
    response.raise_for_status()


async def get_phone_verification_code(phone_number: str) -> str:
    from redis.asyncio import Redis

    from zernyshko.core.config import settings

    redis_client = Redis.from_url(settings.redis_url)
    try:
        value = await redis_client.get(f"phone_code:{phone_number}")
        assert value is not None, "no verification code stored for this phone number"
        return value.decode() if isinstance(value, bytes) else value
    finally:
        await redis_client.aclose()


async def store_phone_verification_code(phone_number: str, code: str) -> None:
    """Пишет код напрямую в Redis, минуя POST /users/phone/code — нужно в
    тестах, где для одного номера требуется несколько подтверждений подряд
    и настоящий rate-limit на отправку (1/60с) мешал бы сценарию."""

    from redis.asyncio import Redis

    from zernyshko.core.config import settings

    redis_client = Redis.from_url(settings.redis_url)
    try:
        await redis_client.set(f"phone_code:{phone_number}", code, ex=600)
    finally:
        await redis_client.aclose()
