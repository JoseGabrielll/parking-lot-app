from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.logger import logger
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.database.database import get_database_session
from app.backend.database.schema.token_schema import Token
from app.backend.service.auth_service import AuthenticationService

token_router = APIRouter(prefix="/api/auth", tags=['Token'])
DatabaseSession = Annotated[AsyncSession, Depends(get_database_session)]

@token_router.post("/token", response_model=Token)
async def get_access_token(database: DatabaseSession,
                           form_data: OAuth2PasswordRequestForm = Depends()):
    """It gets a new access token based in user credentials

    Args:
        database (DatabaseSession): database session
        form_data (OAuth2PasswordRequestForm, optional): username and password information.

    Raises:
        http_error: invalid user or incorrect credentials
        HTTPException: it returns 400 for generic exceptions

    Returns:
        token: It returns a new jwt access token
    """
    try:
        return await AuthenticationService.get_token(database,
                                                    form_data.username, 
                                                    form_data.password)
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        logger.error(error)
        raise HTTPException(status_code=400, detail={"title": "Error", "message": "Error while trying to get token."})

                           
    

