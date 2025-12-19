from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.middleware.auth import JwtHandler

from .models import UserRegister, UserLogin, UserResponse
from .repository import AuthRepository
from .service import AuthService

import logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/auth/register")
async def register_user(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    repository = AuthRepository(db)
    service = AuthService()
    
    existing_user = await repository.get_user_by_username(user_data.username)
    if existing_user:
        logger.info(f"Registration failed: username already exists: {user_data.username}")
        return JSONResponse(
            content={"error": "Username already exists"},
            status_code=400
        )
    
    existing_email = await repository.get_user_by_email(user_data.email)
    if existing_email:
        logger.info(f"Registration failed: email already exists: {user_data.email}")
        return JSONResponse(
            content={"error": "Email already exists"},
            status_code=400
        )
    
    password_hash = service.hash_password(user_data.password)
    
    user = await repository.create_user(
        username=user_data.username,
        email=user_data.email,
        password_hash=password_hash
    )
    
    logger.info(f"User registered successfully: {user.username}")
    
    return JSONResponse(
        content={
            "message": "User registered successfully",
            "user": user.to_dict()
        },
        status_code=201
    )


@router.post("/auth/login")
async def login_user(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    repository = AuthRepository(db)
    service = AuthService()
    jwt_handler = JwtHandler()
    
    user = await repository.get_user_by_username(credentials.username)
    
    if not user:
        logger.info(f"Login failed: user not found: {credentials.username}")
        return JSONResponse(
            content={"error": "Invalid credentials"},
            status_code=401
        )
    
    is_valid = service.verify_password(
        password=credentials.password,
        password_hash=user.password_hash
    )
    
    if not is_valid:
        logger.info(f"Login failed: invalid password for user: {credentials.username}")
        return JSONResponse(
            content={"error": "Invalid credentials"},
            status_code=401
        )
    
    if not user.is_active:
        logger.info(f"Login failed: user is inactive: {credentials.username}")
        return JSONResponse(
            content={"error": "User is inactive"},
            status_code=403
        )
    
    access_token = jwt_handler.create_access_token(user_id=user.id)
    
    logger.info(f"User logged in successfully: {user.username}")
    
    return JSONResponse(
        content={
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "user": user.to_dict()
        },
        status_code=200
    )


@router.get("/auth/user/{user_id}")
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    repository = AuthRepository(db)
    
    user = await repository.get_user_by_id(user_id)
    
    if not user:
        logger.info(f"User not found: {user_id}")
        return JSONResponse(
            content={"error": "User not found"},
            status_code=404
        )
    
    return JSONResponse(
        content=user.to_dict(),
        status_code=200
    )
