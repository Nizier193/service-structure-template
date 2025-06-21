# Module service logic there

from typing import Optional
from redis import Redis

class PingService():
    def __init__(self, cache: Redis) -> None:
        self.cache = cache

    def set_ping(self, id: str):
        self.cache.setex(id, 100, f"Ping №{id}")
    
    def get_ping(self, id: str) -> Optional[str]:
        result: bytes = self.cache.getex(id)

        if not result:
            return None
        
        return result.decode("utf-8")