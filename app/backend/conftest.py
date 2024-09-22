from fastapi.testclient import TestClient
import pytest

import app.backend.database.database as database
from app.backend.app import create_app
from app.backend.config import AppTestConfig
from app.backend.database.database import get_database_session

@pytest.fixture
def test_app():
    app = create_app(config=AppTestConfig())
    client = TestClient(app)

    yield client
    database.engine.dispose()


def exec_database_function(db_func, *args):
    """It receives and execute a database function
    Args:
        db_func (function): database function

    Returns:
        _type_: the function result
    """
    return db_func(*args, get_database_session())