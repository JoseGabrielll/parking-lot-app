from typing import Any
from fastapi import HTTPException
from sqlmodel import Session
from app.backend.database.models.user_model import User
from app.backend.database.dao.user_dao import UserDAO
from app.backend.service.auth_service import AuthenticationService


class UserService:
    
    @staticmethod
    async def create_user(user: User) -> User:
        user.id = None
        user.password = AuthenticationService.generate_password_hash(user.password)
        return await UserDAO.create_user(user)
    
    @staticmethod
    async def get_user_by_field(attribute: str, value: Any) -> User:
        UserService.validate_attribute(attribute)
        
        user = await UserDAO.get_user_by_field(attribute, value)
        if not user:
            raise HTTPException(status_code=404, detail={"title": "Error", "message": "User not found!"})
        return user.model_dump(exclude={"password"})
    
    @staticmethod
    def validate_attribute(attribute: str) -> User:
        if not hasattr(User, attribute):
            raise ValueError(f"The attribute {attribute} does not exist in User model")