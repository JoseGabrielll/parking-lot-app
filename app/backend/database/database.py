from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.backend.settings import app_settings 
from sqlalchemy.pool import StaticPool

engine = None
SessionLocal = None

def connect_db():
    global engine
    global SessionLocal

    if 'sqlite' in app_settings.DB_SERVER:
        engine = create_async_engine(app_settings.DB_SERVER, 
                                     connect_args={"check_same_thread": False},
                                     poolclass=StaticPool)
    else:  # pragma: no cover
        engine = create_async_engine(app_settings.DB_SERVER, 
                                     pool_pre_ping=True)
    
    SessionLocal = sessionmaker(
        engine, 
        class_=AsyncSession, 
        autocommit=False, 
        autoflush=False, 
        expire_on_commit=False
    )

    return engine

def get_metadata():
    from app.backend.database.models.car_model import Car
    from app.backend.database.models.monthly_car_model import MonthlyCar
    from app.backend.database.models.parking_lot_model import ParkingLot, ParkingLotHistory
    from app.backend.database.models.user_model import User

    return SQLModel.metadata

async def get_database_session():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def upgrade_db():
    from alembic import command
    from alembic.config import Config

    alembic_config = Config("alembic.ini")
    alembic_config.attributes["configure_logger"] = False
    alembic_config.attributes["connection"] = engine
    command.upgrade(alembic_config, "head")
