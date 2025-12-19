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
        new_uuid = str(uuid4()) # Новый айдишник

        model = PingConnectionsORM(
            id = new_uuid,
            text = text
        )
        
        logger.debug(f"Пихаем ping в базу с ID={new_uuid}")

        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)  # Обновляем объект после коммита

        
        logger.debug(f"Запись с ID={new_uuid} добавлена")
        return model


    # В качестве ID - UUID4
    async def get_ping_by_id(self, id: str) -> Optional[dict]:
        status = check_is_valid_uuid(id)
        if not status:
            return None

        logger.debug(f"Ищем запись по id={id}")
        query = (
            select(PingConnectionsORM)
            .filter(PingConnectionsORM.id == id)
        )
        result = await self.db.execute(query)
        logger.debug(f"result: {result}")
        ping = result.scalar_one_or_none()

        if not ping:
            logger.debug(f"Запись не найдена: {ping}")
            return None
        
        logger.debug(f"Найдена запись: {ping}")
        return ping.to_dict()


    async def get_ping_paginated(self, size: int, page: int):
        offset = (page - 1) * size
        
        query = (
            select(PingConnectionsORM)
            .order_by(PingConnectionsORM.created_at.desc())  # Сортируем по времени создания (новые первыми)
            .offset(offset)
            .limit(size)
        )
        result = await self.db.execute(query)
        pings = result.scalars().all()

        logger.debug(f"Найдено всего: {len(pings)} ping-ов.")
        
        # Преобразуем в словари
        return [ping.to_dict() for ping in pings]