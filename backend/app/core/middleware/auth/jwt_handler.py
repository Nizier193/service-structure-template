import logging
from datetime import datetime, timedelta
from typing import Optional
import jwt

from core.config import config

logger = logging.getLogger(__name__)


class JwtHandler:
    # Работа с JWT токенами
    
    def __init__(self):
        self.secret_key = config.JWT_SECRET_KEY
        self.algorithm = config.JWT_ALGORITHM
        self.expire_minutes = config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    
    def create_access_token(self, user_id: str) -> str:
        # Создает JWT токен для пользователя
        
        expire_time = datetime.utcnow() + timedelta(minutes=self.expire_minutes)
        
        payload = {
            "user_id": user_id,
            "exp": expire_time,
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(
            payload=payload,
            key=self.secret_key,
            algorithm=self.algorithm
        )
        
        logger.debug(f"JWT token created for user: {user_id}")
        return token
    
    def decode_access_token(self, token: str) -> Optional[str]:
        # Декодирует JWT токен и возвращает user_id
        
        try:
            payload = jwt.decode(
                jwt=token,
                key=self.secret_key,
                algorithms=[self.algorithm]
            )
            
            user_id = payload.get("user_id")
            
            if not user_id:
                logger.debug("Token payload missing user_id")
                return None
            
            logger.debug(f"JWT token decoded for user: {user_id}")
            return user_id
            
        except jwt.ExpiredSignatureError:
            logger.debug("JWT token expired")
            return None
            
        except jwt.InvalidTokenError:
            logger.debug("Invalid JWT token")
            return None

