from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.database.database import get_database_session
from app.backend.database.models.user_model import User
from app.backend.service.auth_service import AuthenticationService


DatabaseSession = Annotated[AsyncSession, Depends(get_database_session)]
AuthUser = Annotated[User, Depends(AuthenticationService.get_current_user)]
