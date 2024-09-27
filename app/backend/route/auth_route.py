from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.backend.database.database import get_database_session
from app.backend.database.schema.token_schema import Token
from app.backend.service.auth_service import AuthenticationService

token_router = APIRouter(prefix="/auth", tags=['Token'])

@token_router.post("/token", response_model=Token)
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends(), 
                           database: Session = Depends(get_database_session)):
    return await AuthenticationService.get_token(form_data.username, form_data.password)
                           
    

