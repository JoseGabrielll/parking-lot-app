import re
import pytest

from app.backend.database.models.user_model import User
from app.backend.tests.utils.mock_utils import mock_user


@pytest.mark.anyio
async def test_get_token_success_e2e(test_app, async_session):
    user = User(email="dummy3@gmail.com", username="dummy12345", password="1234567")
    user_db = await mock_user(async_session, user)

    data = {
        "username": user_db.get("username"),
        "password": "1234567"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = await test_app.post("/api/auth/token", data=data, headers=headers)

    assert response.status_code == 200
    assert response.json().get("token_type") == "Bearer"

    jwt_regex = re.compile(r'^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$')
    assert jwt_regex.match(response.json().get("access_token"))


@pytest.mark.anyio
async def test_get_token_invalid_user_e2e(test_app):
    data = {
        "username": "invaliduser",
        "password": "invalidpassword"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = await test_app.post("/api/auth/token", data=data, headers=headers)

    assert response.status_code == 401
    assert response.json().get("detail") == {"title": "Unauthorized", "message": "Incorrect username or password"}


@pytest.mark.anyio
async def test_get_token_invalid_password_e2e(test_app, async_session):
    user = User(email="dummy4@gmail.com", username="dummy4", password="1234567")
    user_db = await mock_user(async_session, user)

    data = {
        "username": user_db.get("username"),
        "password": "invalidpassword"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = await test_app.post("/api/auth/token", data=data, headers=headers)

    assert response.status_code == 401
    assert response.json().get("detail") == {"title": "Unauthorized", "message": "Incorrect username or password"}
