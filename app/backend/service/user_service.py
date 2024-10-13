from typing import Any
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.database.models.user_model import User
from app.backend.database.dao.user_dao import UserDAO
from app.backend.database.schema.user_schema import UserPayload
from app.backend.service.auth_service import AuthenticationService


class UserService:
    
    @staticmethod
    async def create_user(database: AsyncSession, user_payload: UserPayload) -> User:
        """It creates a new user

        Args:
            database (AsyncSession): database session
            user_payload (UserPayload): user payload
        
        Raises:
            HTTPException: It raises an exception if the user already exists

        Returns:
            User: database user
        """
        user = User(**user_payload.model_dump())
        db_user = await UserDAO.get_user_by_username_or_email(database, user)
        if db_user:
            raise HTTPException(status_code=409, detail={"title": "Error", "message": "User already exists!"})
        
        user.password = AuthenticationService.generate_password_hash(user.password)
        return await UserDAO.create_user(database, user)
    
    @staticmethod
    async def get_user_by_field(database: AsyncSession, attribute: str, value: Any) -> User:
        """It gets a user based in a user field

        Args:
            database (AsyncSession): database session
            attribute (str): user attribute
            value (Any): attribute value

        Raises:
            HTTPException: It raises an exception if the user is not found in database

        Returns:
            User: database user
        """
        UserService.validate_attribute(attribute)
        
        user = await UserDAO.get_user_by_field(database, attribute, value)
        if not user:
            raise HTTPException(status_code=404, detail={"title": "Error", "message": "User not found!"})
        return user.model_dump(exclude={"password"})
    
    @staticmethod
    def validate_attribute(attribute: str) -> User:
        """It validates if the attribute is valid for User model

        Args:
            attribute (str): attribute name

        Raises:
            ValueError: It raises an exception if attribute is invalid

        """
        if not hasattr(User, attribute):
            raise ValueError(f"The attribute {attribute} does not exist in User model")