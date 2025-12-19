from fastapi import Body, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from core.cache import get_cache
from core.database import get_db
from core.middleware.auth import get_current_user_id

from .repository import PingRepository
from .service import PingService

import logging
logger = logging.getLogger(__name__)

router = APIRouter()

# Обычный пинг, без привата
@router.get("/ping")
async def ping(
    db: AsyncSession = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    repository = PingRepository(db)
    service = PingService(cache)

    model = await repository.insert_ping()
    await service.set_ping(str(model.id))

    return JSONResponse(
        content={
            "status": "Server is online",
            "connection": model.to_dict()
        },
        status_code=200
    )


@router.get("/ping/single/{ping_id}")
async def get_ping(
    ping_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    repository = PingRepository(db)
    service = PingService(cache)

    ping = await repository.get_ping_by_id(ping_id)
    cache_ping = await service.get_ping(ping_id)

    if not ping:
        logger.info(f"Ping not found: {ping_id}")
        return JSONResponse(
            content={"error": "not found"},
            status_code=404
        )

    ping["cache"] = {"cached_ping": cache_ping}
    ping["requested_by"] = user_id

    return JSONResponse(
        content=ping,
        status_code=200
    )


@router.get("/ping/list")
async def get_ping_paginated(
    size: int = Query(default=10e10, gt=0),
    page: int = Query(default=1, gt=0),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    repository = PingRepository(db)
    result = await repository.get_ping_paginated(size, page)

    logger.info(f"User {user_id} requested {len(result)} pings (page={page}, size={int(size)})")
    return JSONResponse(
        content={
            "requested_by": user_id,
            "pings": result,
            "count": len(result)
        },
        status_code=200
    )