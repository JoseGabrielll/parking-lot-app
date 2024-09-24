from fastapi import HTTPException
from sqlmodel import Session
from app.backend.database.models.user_model import User
from app.backend.database.dao.user_dao import UserDAO


class UserService:
    
    @staticmethod
    def create_user(user: User) -> User:
        return UserDAO.create_user(user)
    
    @staticmethod
    def get_user_by_id(id: int) -> User:
        user = UserDAO.get_user_by_id(id)
        if not user:
            raise HTTPException(status_code=404, detail={"title": "Error", "message": "User not found!"})

        return user