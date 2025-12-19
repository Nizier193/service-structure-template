import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.logger import setup_logging, get_logger
from core.middleware.tracing import TracingMiddleware
from src.head_router import router
from core.cache import init_redis, close_redis
from core.database import engine
from core.database import close_db
from core.config import config
from src.modules.ping.schemas import Base as PingBase
from src.modules.auth.schemas import Base as AuthBase

# Инициализируем логирование (консоль + ротация файлов)
setup_logging(
    level=config.LOG_LEVEL
)
logger = get_logger(__name__)
logger.debug("Starting with configuration:")
for key, value in config.model_dump().items():
    logger.debug(f"{key} = {value}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()
    
    async with engine.begin() as conn:
        await conn.run_sync(PingBase.metadata.create_all)
        await conn.run_sync(AuthBase.metadata.create_all)

    yield

    await close_redis()
    await close_db()


app = FastAPI(lifespan=lifespan)

# Подключаем трассировку запросов
app.add_middleware(TracingMiddleware)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=config.HOST,
        port=config.PORT
    )