import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import ASGITransport, AsyncClient
from sqlalchemy.pool import StaticPool

from app.backend.app import create_app
from app.backend.database.database import AsyncSession, create_test_tables, get_database_session
from app.backend.settings import AppSettings


@pytest_asyncio.fixture(name="async_session", scope="function")
async def session_fixture():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", 
                                connect_args={"check_same_thread": False},
                                poolclass=StaticPool)

    await create_test_tables(engine)
    async with AsyncSession(engine) as async_session:
        yield async_session


@pytest_asyncio.fixture(scope="function")  
async def test_app(async_session: AsyncSession):
    def get_session_override():  
        return async_session

    app = create_app(AppSettings(db_server="sqlite+aiosqlite:///:memory:",
                                 secret_key="TEST123",
                                 algorithm="HS256",
                                 access_token_expire_minutes="5"))
    app.dependency_overrides[get_database_session] = get_session_override
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest.fixture
def anyio_backend():
    return 'asyncio'
