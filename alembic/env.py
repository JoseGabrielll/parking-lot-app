import asyncio

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy import pool

from app.backend.database.database import get_metadata
from app.backend.settings import AppSettings


config = context.config
config.set_main_option("sqlalchemy.url", AppSettings().DB_SERVER)
target_metadata = get_metadata()


def run_migrations_online():
    connectable = context.config.attributes.get("connection", None)

    if connectable is None:
        connectable = AsyncEngine(
            engine_from_config(
                context.config.get_section(context.config.config_ini_section),
                prefix="sqlalchemy.",
                poolclass=pool.NullPool,
                future=True,
            )
        )

    if isinstance(connectable, AsyncEngine):
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.ensure_future(run_async_migrations(connectable))
        else:
            loop.run_until_complete(run_async_migrations(connectable))
    else:
        with connectable.connect() as connection:
            do_run_migrations(connection)


async def run_async_migrations(connectable):
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection):
    try:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()
    except Exception as error:
        print(error)
        raise error

run_migrations_online()