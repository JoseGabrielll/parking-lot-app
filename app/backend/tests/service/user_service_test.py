import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock, patch

from app.backend.database.dao.user_dao import UserDAO
from app.backend.database.models.user_model import User
from app.backend.service.user_service import UserService


def test_validate_attribute_error():
    invalid_attribute = "dummy"
    with pytest.raises(ValueError) as value_error:
        UserService.validate_attribute(invalid_attribute)
        assert value_error == "The attribute {invalid_attribute} does not exist in User model"


@patch.object(UserDAO, "get_user_by_field")
async def test_user_not_found(mock_get_user_dao):
    mock_get_user_dao.return_value = None

    with pytest.raises(HTTPException) as http_error:
        await UserService.get_user_by_field(MagicMock(), "id", 1)
        assert http_error.status_code == 404
        assert http_error.detail == {"title": "Error", "message": "User not found!"}


@patch.object(UserDAO, "get_user_by_field")
async def test_return_user_without_password(mock_get_user_dao):
    mock_get_user_dao.return_value = User(id=1, 
                                          email="dummy@test.com", 
                                          username="dummy",
                                          password="12345")
    
    user = await UserService.get_user_by_field(MagicMock(), "id", 1)
    assert 'password' not in user.keys()
    assert 'email' in  user.keys()
    assert 'username' in  user.keys()
    assert 'is_active' in  user.keys()
    

