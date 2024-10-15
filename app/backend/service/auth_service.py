from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import encode, decode
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.database.database import get_database_session
from app.backend.database.dao.user_dao import UserDAO
from app.backend.database.models.user_model import User
from app.backend.database.schema.token_schema import Token
from app.backend.settings import AppSettings

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

class AuthenticationService():
    ''' Authentication service class with user business rules '''

    @staticmethod
    def generate_password_hash(password: str) -> str:
        """It gets the password and generate a hashed password

        Args:
            password (str): raw password

        Returns:
            str: hashed password
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """It checks if the password matches with the hashed password

        Args:
            password (str): raw password
            hashed_password (str): hashed password

        Returns:
            bool: True if maches, False otherwise
        """
        return pwd_context.verify(password, hashed_password)

    @staticmethod
    async def get_token(database: AsyncSession, username: str, password: str) -> Token:
        """It checks the user credentials and returns an access token

        Args:
            username (str): username
            password (str): password

        Raises:
            HTTPException: It raises an exception if the user is invalid or incorrect credential 

        Returns:
            Token: access token
        """
        user = await UserDAO.get_user_by_field(database, 'username', username)
        if not user or not AuthenticationService.verify_password(password, user.password):
            raise HTTPException(
                status_code=401,
                detail={"title": "Unauthorized", "message": "Incorrect username or password"}
            )

        access_token = AuthenticationService.create_access_token({'sub': user.username}) # TODO: add 'role' claim in token
        return {'access_token': access_token, 'token_type': 'Bearer'}

    @staticmethod
    def create_access_token(data: dict):
        """It generates a new token

        Args:
            data (dict): information to be added into token

        Returns:
            token: jwt token
        """
        final_date = datetime.now() + timedelta(minutes=AppSettings().ACCESS_TOKEN_EXPIRE_MINUTES)
        data['exp'] = final_date.timestamp()
        return encode(data, AppSettings().SECRET_KEY, algorithm=AppSettings().ALGORITHM)

    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        database: Annotated[AsyncSession, Depends(get_database_session)]
    ) -> User:
        """It decodes the token and gets the related user

        Args:
            token (T_Token): jwt token provided via /auth/token
            database (DatabaseSession): database session

        Raises:
            HTTPException: it raises an exception if the user is None
            HTTPException: it raises an exception if the user is not in db
            HTTPException: it raises an exception if the token is invalid

        Returns:
            User: user from database
        """
        try:
            credentials_exception = HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            payload = decode(
                token,
                AppSettings().SECRET_KEY,
                algorithms=[AppSettings().ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            user = await UserDAO.get_user_by_field(database, 'username', username)
            if user is None:
                raise credentials_exception
            return user
        except InvalidTokenError as error:
            raise credentials_exception from error
        except Exception as error:
            raise error from error
