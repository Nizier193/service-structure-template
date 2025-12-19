import logging
from typing import Optional
from fastapi import Header, HTTPException, status

from .jwt_handler import JwtHandler

logger = logging.getLogger(__name__)


def get_current_user_id(authorization: Optional[str] = Header(None)) -> str:
    """
    Dependency для получения user_id из JWT токена
    
    Использование:
        @router.get("/protected")
        async def protected_endpoint(user_id: str = Depends(get_current_user_id)):
            return {"user_id": user_id}
    """
    
    if not authorization:
        logger.info("Missing Authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required"
        )
    
    if not authorization.startswith("Bearer "):
        logger.info("Invalid Authorization header format")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization format. Use: Bearer <token>"
        )
    
    token = authorization.replace("Bearer ", "")
    
    jwt_handler = JwtHandler()
    user_id = jwt_handler.decode_access_token(token)
    
    if not user_id:
        logger.info("Invalid or expired JWT token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    logger.debug(f"User authenticated: {user_id}")
    return user_id

