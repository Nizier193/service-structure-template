from typing import Optional
from redis.asyncio import Redis

class PingService:
    def __init__(self, cache: Redis) -> None:
        self.cache = cache

    async def set_ping(self, id: str):
        await self.cache.setex(
            name=f"ping:{id}",
            time=100,
            value=f"Ping №{id}"
        )
    
    async def get_ping(self, id: str) -> Optional[str]:
        """Достаём пинг из кеша"""
        result = await self.cache.get(f"ping:{id}")
        
        if not result:
            return None
        
        return result 