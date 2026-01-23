import asyncio
from logging.config import fileConfig
from pathlib import Path
import sys

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config


backend_app_path = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(backend_app_path))

from core.config import config as app_config
from src.modules.ping.schemas import Base as PingBase
from src.modules.auth.schemas import Base as AuthBase


alembic_config = context.config

if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)


target_metadata = [
    PingBase.metadata,
    AuthBase.metadata,
]


def get_database_url() -> str:
    database_url = app_config.DATABASE_URI
    return database_url


def run_migrations_offline() -> None:
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = async_engine_from_config(
        configuration=alembic_config.get_section(alembic_config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=get_database_url(),
    )

    asyncio.run(run_async_migrations(connectable))


async def run_async_migrations(connectable) -> None:
    async with connectable.connect() as connection:
        await connection.run_sync(configure_migration_context)

        await connection.run_sync(run_sync_migrations)

    await connectable.dispose()


def configure_migration_context(connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )


def run_sync_migrations(connection) -> None:
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


