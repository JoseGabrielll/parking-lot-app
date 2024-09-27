import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.backend.database.database import get_metadata
import app.backend.database.database as db
from app.backend.settings import app_settings


loop = asyncio.get_event_loop()

if db.engine is None:
    loop.run_until_complete(db.connect_db())

alembic_config = context.config
alembic_config.set_main_option("sqlalchemy.url", app_settings.DB_SERVER)

if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

target_metadata = get_metadata()

def run_migrations_offline() -> None:
    url = alembic_config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        alembic_config.get_section(alembic_config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    if loop.is_running():
        asyncio.ensure_future(run_async_migrations())
    else:
        loop.run_until_complete(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
