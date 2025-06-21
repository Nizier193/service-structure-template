from fastapi import Body, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from redis import Redis
from sqlalchemy.orm import Session

from core.cache import get_cache
from core.database import get_db

from .repository import PingRepository
from .service import PingService

router = APIRouter()

@router.get("/ping")
def ping(
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    repository = PingRepository(db)
    service = PingService(cache)

    model = repository.insert_ping()
    service.set_ping(str(model.id))

    return JSONResponse(
        content={
            "status": "Server is online",
            "connection": model.to_dict()
        },
        status_code=200
    )


@router.get("/ping/single/{ping_id}")
def get_ping(
    ping_id: str,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    repository = PingRepository(db)
    service = PingService(cache)

    ping = repository.get_ping_by_id(ping_id)
    cache_ping = service.get_ping(ping_id)

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
def get_ping_paginated(
    size: int = Query(default=10e10, gt=0),
    page: int = Query(default=1, gt=0),
    db: Session = Depends(get_db)
):
    repository = PingRepository(db)
    result = repository.get_ping_paginated(size, page)

    return JSONResponse(
        content=result,
        status_code=200
    )