import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context
from app.backend.database.database import get_metadata, connect_db
from app.backend.settings import app_settings
from app.backend.database.database import engine as raw_engine


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
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    engine = raw_engine if raw_engine else connect_db()

    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await engine.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
