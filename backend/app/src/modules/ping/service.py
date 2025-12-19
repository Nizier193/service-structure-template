import logging
from typing import Optional
from redis.asyncio import Redis

logger = logging.getLogger(__name__)


class PingService:
    def __init__(self, cache: Redis) -> None:
        self.cache = cache

    async def set_ping(self, id: str):
        cache_key = f"ping:{id}"
        
        await self.cache.setex(
            name=cache_key,
            time=100,
            value=f"Ping №{id}"
        )
        
        logger.debug(f"Cached ping: {cache_key}")
    
    async def get_ping(self, id: str) -> Optional[str]:
        cache_key = f"ping:{id}"
        result = await self.cache.get(cache_key)
        
        if not result:
            logger.debug(f"Cache miss: {cache_key}")
            return None
        
        logger.debug(f"Cache hit: {cache_key}")
        return result 