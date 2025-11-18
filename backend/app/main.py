import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from logging import config 
from pathlib import Path

# Инициализируем конфиг логов сразу
config.fileConfig(Path(__file__).parent / "logger.ini")

from src.head_router import router

from core.cache import init_redis, close_redis
from core.database import engine
from core.database import close_db
from core.config import config

from src.modules.ping.schemas import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await close_redis()
    await close_db()


app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=config.HOST,
        port=config.PORT
    )