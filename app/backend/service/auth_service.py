from fastapi import HTTPException
from datetime import datetime, timedelta
from jwt import encode
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo

from app.backend.database.dao.user_dao import UserDAO
from app.backend.database.schema.token_schema import Token
from app.backend.settings import AppSettings

pwd_context = PasswordHash.recommended()

class AuthenticationService():

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
    async def get_token(username: str, password: str) -> Token:
        """It checks the user credentials and returns an access token

        Args:
            username (str): username
            password (str): password

        Raises:
            HTTPException: It raises an exception if the user is invalid or incorrect credential 

        Returns:
            Token: access token
        """
        user = await UserDAO.get_user_by_field('username', username)
        if not user or not AuthenticationService.verify_password(password, user.password):
            raise HTTPException(
                status_code=401, 
                detail={"title": "Unauthorized", "message": "Incorrect username or password"}
            )
        
        access_token = AuthenticationService.create_access_token({'sub': user.username}) # TODO: add 'role' claim in token
        return {'access_token': access_token, 'token_type': 'Bearer'}

    @staticmethod
    def create_access_token(data: dict):
        data['exp'] = datetime.now() + timedelta(minutes=AppSettings().ACCESS_TOKEN_EXPIRE_MINUTES)
        return encode(data, AppSettings().SECRET_KEY, algorithm=AppSettings().ALGORITHM)