# SQLAlchemy schemas there

from sqlalchemy import (
    UUID,
    Column,
    Integer,
    Text,
    TIMESTAMP
)
from sqlalchemy.orm import DeclarativeBase

from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    pass


class PingConnections(Base):
    __tablename__ = "ping_connections"
    
    id = Column("connection_number", UUID, primary_key=True)
    text = Column("text", Text)  # Для примера просто информация
    created_at = Column("created_at", DateTime, default=func.now())  # Время создания

    def to_dict(self):
        return {
            "id": str(self.id),
            "text": self.text,
            "time": self.created_at.isoformat() if self.created_at else None,
        }