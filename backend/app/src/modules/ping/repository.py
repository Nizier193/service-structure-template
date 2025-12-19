# Database class logic there

from ast import Dict
from typing import Optional
from uuid import uuid4
from .schemas import PingConnections as PingConnectionsORM
from .schemas import Base

from .support.uuid_module import check_is_valid_uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import logging
logger = logging.getLogger(__name__)

class PingRepository():
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def insert_ping(self, text: str = ""):
        new_uuid = str(uuid4())

        model = PingConnectionsORM(
            id=new_uuid,
            text=text
        )

        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)

        return model


    async def get_ping_by_id(self, id: str) -> Optional[dict]:
        status = check_is_valid_uuid(id)
        if not status:
            logger.debug(f"Invalid UUID format: {id}")
            return None

        query = (
            select(PingConnectionsORM)
            .filter(PingConnectionsORM.id == id)
        )
        result = await self.db.execute(query)
        ping = result.scalar_one_or_none()

        if not ping:
            return None
        
        return ping.to_dict()


    async def get_ping_paginated(self, size: int, page: int):
        offset = (page - 1) * size
        
        query = (
            select(PingConnectionsORM)
            .order_by(PingConnectionsORM.created_at.desc())
            .offset(offset)
            .limit(size)
        )
        result = await self.db.execute(query)
        pings = result.scalars().all()

        logger.debug(f"Fetched {len(pings)} records (page={page}, limit={size})")
        
        return [ping.to_dict() for ping in pings]