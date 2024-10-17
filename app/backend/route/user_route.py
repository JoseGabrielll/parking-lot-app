from fastapi import APIRouter, HTTPException
from fastapi.logger import logger
from fastapi.security import OAuth2PasswordBearer

from app.backend.database.schema.user_schema import UserPayload, UserSchema
from app.backend.database.models.user_model import UserRoles
from app.backend.service.user_service import UserService
from app.backend.tests.utils.decorators import validate_user_access
from app.backend.utils.annotated_types import DatabaseSession, AuthUser


user_router = APIRouter(prefix="/api/user", tags=['User'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


@user_router.post("", response_model=UserSchema, status_code=201)
@validate_user_access([UserRoles.ADMIN.value])
async def create_user(
        user_payload: UserPayload,
        database: DatabaseSession,
        user: AuthUser
    ) -> UserSchema:
    """It creates an user

    Args:
        user (User): user schema
        database (Session, optional): database session. Defaults to Depends(get_database).

    Raises:
        http_error: it returns 409 if user already exists
        HTTPException: it returns 400 for generic exceptions

    Returns:
        UserSchema: user object from database
    """
    try:
        return await UserService.create_user(database, user_payload)
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        logger.error(error)
        raise HTTPException(
            status_code=400,
            detail={'title': 'Error', 'message': 'Error while trying to create user.'}
            ) from error


@user_router.get("/{id}", response_model=UserSchema)
@validate_user_access([UserRoles.ADMIN.value, UserRoles.EMPLOYEE.value])
async def get_user(
        id: int,
        database: DatabaseSession,
        user: AuthUser
    ) -> UserSchema:
    """It gets the user by id

    Args:
        id (int): user id
        database (Session): database session. Defaults to Depends(get_database).

    Raises:
        http_error: it returns 404 if user doesn`t exists
        HTTPException: it returns 400 for generic exceptions

    Returns:
        UserSchema: user object from database
    """
    try:
        return await UserService.get_user_by_field(database, 'id', id)
    except HTTPException as http_error:
        raise http_error
    except ValueError as value_error:
        logger.error(value_error)
        raise HTTPException(
            status_code=400,
            detail={"title": "Error", "message": "Value error"}
            ) from value_error
    except Exception as error:
        logger.error(error)
        raise HTTPException(
            status_code=400,
            detail={"title": "Error", "message": "Error while trying to get user."}
            ) from error
