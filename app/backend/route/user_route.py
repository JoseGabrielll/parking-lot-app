from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.database.database import get_database_session
from app.backend.database.models.user_model import User
from app.backend.database.schema.user_schema import UserPayload
from app.backend.service.user_service import UserService


user_router = APIRouter(prefix="/api/user", tags=['User'])
DatabaseSession = Annotated[AsyncSession, Depends(get_database_session)]

@user_router.post("", response_model=User, status_code=201)
async def create_user(user: UserPayload, database: DatabaseSession) -> User:
    """It creates an user

    Args:
        user (User): user schema
        database (Session, optional): database session. Defaults to Depends(get_database).

    Raises:
        http_error: it returns 409 if user already exists
        HTTPException: it returns 400 for generic exceptions

    Returns:
        User: user object from database
    """
    try:
        return await UserService.create_user(database, user)
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        logger.error(error)
        raise HTTPException(status_code=400, detail={"title": "Error", "message": "Error while trying to create user."})


@user_router.get("/{id}", response_model=User)
async def get_user(id: int, database: DatabaseSession) -> User:
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
        return await UserService.get_user_by_field(database, 'id', id)
    except HTTPException as http_error:
        raise http_error
    except ValueError as value_error:
        logger.error(value_error)
        raise HTTPException(status_code=400, detail={"title": "Error", "message": "Value error"})
    except Exception as error:
        logger.error(error)
        raise HTTPException(status_code=400, detail={"title": "Error", "message": "Error while trying to get user."})