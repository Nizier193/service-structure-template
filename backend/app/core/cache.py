from redis.asyncio import Redis
from typing import Optional
from .config import config

redis_client: Optional[Redis] = None

async def init_redis():
    global redis_client

    redis_client = await Redis(
        host=config.CACHE_HOST,
        port=config.CACHE_PORT,
        decode_responses=True,  # Автоматически декодирует в строки
        encoding="utf-8"
    )

    await redis_client.ping()  # Проверка подключения

async def close_redis():
    global redis_client

    if redis_client:
        await redis_client.close()

async def get_cache() -> Redis:
    if redis_client is None:
        raise RuntimeError("Redis not initialized! Call init_redis() first.")
    return redis_client