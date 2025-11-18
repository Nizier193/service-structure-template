from fastapi import Body, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from core.cache import get_cache
from core.database import get_db

from .repository import PingRepository
from .service import PingService

# Логгер
import logging
logger = logging.getLogger(__name__)

router = APIRouter()

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
    db: AsyncSession = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    repository = PingRepository(db)
    service = PingService(cache)

    ping = await repository.get_ping_by_id(ping_id)
    cache_ping = await service.get_ping(ping_id)

    if not ping:
        return JSONResponse(
            content={"error": "not found"},
            status_code=404
        )

    ping["cache"] = {"cached_ping": cache_ping}

    return JSONResponse(
        content=ping,
        status_code=200
    )


@router.get("/ping/list")
async def get_ping_paginated(
    size: int = Query(default=10e10, gt=0),
    page: int = Query(default=1, gt=0),
    db: AsyncSession = Depends(get_db)
):
    repository = PingRepository(db)
    result = await repository.get_ping_paginated(size, page)

    return JSONResponse(
        content=result,
        status_code=200
    )