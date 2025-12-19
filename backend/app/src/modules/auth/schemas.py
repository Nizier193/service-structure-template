# SQLAlchemy ORM модели

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from uuid import uuid4


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    
    id = Column("id", String, primary_key=True, default=lambda: str(uuid4()))
    username = Column("username", String, unique=True, nullable=False)
    email = Column("email", String, unique=True, nullable=False)
    password_hash = Column("password_hash", String, nullable=False)
    is_active = Column("is_active", Boolean, default=True)
    created_at = Column("created_at", DateTime, default=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
