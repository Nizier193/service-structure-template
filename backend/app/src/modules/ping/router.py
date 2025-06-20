from fastapi import Body, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from sqlalchemy.orm import Session

from core.database import get_db
from .repository import PingRepository

router = APIRouter()

@router.get("/ping")
def ping(
    db: Session = Depends(get_db),
):
    repository = PingRepository(db)
    model = repository.insert_ping()

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
    db: Session = Depends(get_db)
):
    repository = PingRepository(db)
    ping = repository.get_ping_by_id(ping_id)

    if not ping:
        return JSONResponse(
            content={"error": "not found"},
            status_code=404
        )

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