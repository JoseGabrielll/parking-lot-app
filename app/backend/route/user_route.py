from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.backend.database.database import get_database
from app.backend.database.models.user_model import User
from app.backend.service.user_service import UserService


user_router = APIRouter(prefix="/api/user")

@user_router.post("/", response_model=User, tags=['User'], status_code=201)
async def create_user(user: User, database: Session = Depends(get_database)) -> User:
    """It creates a user

    Args:
        user (User): user schema
        database (Session, optional): database session. Defaults to Depends(get_database).

    Raises:
        HTTPException: it returns 400 for generic exceptions

    Returns:
        User: user object from database
    """
    try:
        return UserService.create_user(user)
    except Exception as error:
        # TODO: add logger.error here
        raise HTTPException(status_code=400, detail={"title": "Error", "message": "Error while trying to create user."})


@user_router.get("/{id}", response_model=User, tags=['User'])
async def get_user(id: int, database: Session = Depends(get_database)) -> User:
    """It gets the user by id

    Args:
        id (int): user id
        database (Session, optional): database session. Defaults to Depends(get_database).

    Raises:
        http_error: it returns 404 if user doesn`t exists
        HTTPException: it returns 400 for generic exceptions

    Returns:
        User: user object from database
    """
    try:
        return UserService.get_user_by_id(id)
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        # TODO: add logger.error here
        raise HTTPException(status_code=400, detail={"title": "Error", "message": "Error while trying to get user."})