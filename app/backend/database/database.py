from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import create_engine

from app.backend.config import AppConfig

engine = None
SessionLocal = None

def connect_db(config=AppConfig()):
    global engine
    global SessionLocal

    if engine: # pragma: no cover
        engine.dispose()

    if 'sqlite' in config.DB_SERVER:
        engine = create_engine(config.DB_SERVER, 
                               connect_args={"check_same_thread": False},
                               poolclass=StaticPool)
    else: # pragma: no cover
        engine = create_engine(config.DB_SERVER, 
                               pool_pre_ping=True)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_metadata(): # TODO: used by alembic
    from sqlmodel import SQLModel

    from app.backend.database.models.user_model import User

    return SQLModel.metadata


def get_database():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

def get_database_session():
    database = SessionLocal()
    try:
        return database
    finally:
        database.close()

def upgrade_db():
    from alembic import command
    from alembic.config import Config

    alembic_config = Config("alembic.ini")
    alembic_config.attributes["configure_logger"] = False
    alembic_config.attributes["connection"] = engine
    command.upgrade(alembic_config, "head")

