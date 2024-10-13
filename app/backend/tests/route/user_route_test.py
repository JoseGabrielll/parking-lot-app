from unittest.mock import patch
from fastapi import HTTPException
import pytest

from app.backend.database.dao.user_dao import UserDAO
from app.backend.database.models.user_model import User
from app.backend.service.user_service import UserService


async def mock_user(async_session, user: User = User(email="dummy@gmail.com", username="dummy123", password="123456")):
    return await UserDAO.create_user(async_session, user)


@pytest.mark.anyio
async def test_get_user_success_e2e(test_app, async_session):
    user_db = await mock_user(async_session)
    response = await test_app.get(f"/api/user/{user_db.get('id')}")

    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_user_not_found_e2e(test_app):  
    response = await test_app.get("/api/user/1")

    assert response.status_code == 404
    assert response.json().get("detail") == {"title": "Error", "message": "User not found!"}


@pytest.mark.anyio
@patch.object(UserService, "get_user_by_field")
async def test_get_user_value_error_e2e(mock_get_user_by_field, test_app):  
    mock_get_user_by_field.side_effect = ValueError()

    response = await test_app.get("/api/user/1")

    assert response.status_code == 400
    assert response.json().get("detail") == {"title": "Error", "message": "Value error"}


@pytest.mark.anyio
@patch.object(UserDAO, "get_user_by_field")
async def test_get_user_http_exception_e2e(mock_get_user_by_field, test_app):  
    mock_get_user_by_field.return_value = None

    response = await test_app.get("/api/user/1")

    assert response.status_code == 404
    assert response.json().get("detail") == {"title": "Error", "message": "User not found!"}


@pytest.mark.anyio
@patch.object(UserService, "get_user_by_field")
async def test_get_user_general_exception_e2e(mock_get_user_by_field, test_app):  
    mock_get_user_by_field.side_effect = Exception()

    response = await test_app.get("/api/user/1")

    assert response.status_code == 400
    assert response.json().get("detail") == {"title": "Error", "message": "Error while trying to get user."}


@pytest.mark.anyio
async def test_create_user_success_e2e(test_app):
    payload = {
        "username": "dummy123",
        "password": "123456",
        "email": "dummy@test.com"
    }

    response = await test_app.post("/api/user", json=payload)

    assert response.status_code == 201
    assert response.json().get("username") == payload.get("username")
    assert response.json().get("email") == payload.get("email")


@pytest.mark.anyio
async def test_create_user_already_exists_e2e(test_app, async_session):
    user = User(email="dummy2@gmail.com", username="dummy1234", password="1234567")
    user_db = await mock_user(async_session, user)
    payload = {
        "username": user_db.get("username"),
        "password": "123456",
        "email": user_db.get("email")
    }

    response = await test_app.post("/api/user", json=payload)

    assert response.status_code == 409
    assert response.json().get("detail") == {"title": "Error", "message": "User already exists!"}


@pytest.mark.anyio
@patch.object(UserService, "create_user")
async def test_create_user_exception_e2e(mock_create_user, test_app):
    mock_create_user.side_effect = Exception()
    payload = {
        "username": "dummy123",
        "password": "123456",
        "email": "dummy@test.com"
    }

    response = await test_app.post("/api/user", json=payload)

    assert response.status_code == 400
    assert response.json().get("detail") == {"title": "Error", "message": "Error while trying to create user."}


async def test_create_user_invalid_payload_e2e(test_app):
    payload = {"email": "dummy@test.com"}
    response = await test_app.post("/api/user", json=payload)

    assert response.status_code == 422
    assert response.json() == {"detail": "Error on request body. Please check the submitted data and try again."}

