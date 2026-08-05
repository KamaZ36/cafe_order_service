from redis.asyncio import Redis

from zernyshko.infrastructure.verification.base import PhoneVerificationCodeStorage

CODE_TTL_SECONDS = 600


class RedisPhoneVerificationCodeStorage(PhoneVerificationCodeStorage):
    def __init__(self, redis_client: Redis) -> None:
        self._redis = redis_client

    def _key(self, phone_number: str) -> str:
        return f"phone_code:{phone_number}"

    async def create(self, phone_number: str, code: str) -> None:
        await self._redis.set(self._key(phone_number), code, ex=CODE_TTL_SECONDS)

    async def get(self, phone_number: str) -> str | None:
        value = await self._redis.get(self._key(phone_number))
        return value.decode() if isinstance(value, bytes) else value

    async def delete(self, phone_number: str) -> None:
        await self._redis.delete(self._key(phone_number))
