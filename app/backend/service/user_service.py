from typing import Any
from fastapi import HTTPException
from sqlmodel import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.database.models.user_model import User
from app.backend.database.dao.user_dao import UserDAO
from app.backend.database.schema.user_schema import UserPayload
from app.backend.service.auth_service import AuthenticationService


class UserService:
    
    @staticmethod
    async def create_user(database: AsyncSession, user_payload: UserPayload) -> User:
        user = User(**user_payload.model_dump())
        user.password = AuthenticationService.generate_password_hash(user.password)
        return await UserDAO.create_user(database, user)
    
    @staticmethod
    async def get_user_by_field(database: AsyncSession, attribute: str, value: Any) -> User:
        UserService.validate_attribute(attribute)
        
        user = await UserDAO.get_user_by_field(database, attribute, value)
        if not user:
            raise HTTPException(status_code=404, detail={"title": "Error", "message": "User not found!"})
        return user.model_dump(exclude={"password"})
    
    @staticmethod
    def validate_attribute(attribute: str) -> User:
        if not hasattr(User, attribute):
            raise ValueError(f"The attribute {attribute} does not exist in User model")