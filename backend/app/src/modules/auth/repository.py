# Репозиторий для работы с пользователями в БД

import logging
from typing import Optional
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .schemas import User as UserORM

logger = logging.getLogger(__name__)


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(
        self,
        username: str,
        email: str,
        password_hash: str
    ) -> UserORM:
        new_uuid = str(uuid4())
        
        user = UserORM(
            id=new_uuid,
            username=username,
            email=email,
            password_hash=password_hash
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def get_user_by_username(self, username: str) -> Optional[UserORM]:
        query = select(UserORM).filter(UserORM.username == username)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        
        return user
    
    async def get_user_by_email(self, email: str) -> Optional[UserORM]:
        query = select(UserORM).filter(UserORM.email == email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        
        return user
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserORM]:
        query = select(UserORM).filter(UserORM.id == user_id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        
        return user
