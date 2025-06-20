# Database class logic there

from ast import Dict
from typing import Optional
from uuid import uuid4
from .schemas import PingConnections as PingConnectionsORM
from .schemas import Base

from sqlalchemy.orm import Session

class PingRepository():
    def __init__(self, db: Session):
        self.db = db
        Base.metadata.create_all(db.bind)

    
    def insert_ping(self, text: str = ""):
        new_uuid = str(uuid4()) # Новый айдишник

        model = PingConnectionsORM(
            id = new_uuid,
            text = text
        )

        self.db.add(model)
        self.db.commit()

        return model


    # В качестве ID - UUID4
    def get_ping_by_id(self, id: str) -> Optional[Dict]:
        ping = (
            self.db.query(PingConnectionsORM)
            .filter(PingConnectionsORM.id == id)
            .first()
        )

        if not ping:
            return None
        
        return ping.to_dict()


    def get_ping_paginated(self, size: int, page: int):
        offset = (page - 1) * size
        
        pings = (
            self.db.query(PingConnectionsORM)
            .order_by(PingConnectionsORM.created_at.desc())  # Сортируем по времени создания (новые первыми)
            .offset(offset)
            .limit(size)
            .all()
        )
        
        # Преобразуем в словари
        return [ping.to_dict() for ping in pings]