from typing import AsyncGenerator

from sqlalchemy.engine.url import URL, make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import config
from core.logger import get_logger


logger = get_logger(__name__)

engine = create_async_engine(
    config.DATABASE_URI,
    echo=False,  # set True for SQL echo
    future=True,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()


async def close_db():
    await engine.dispose()