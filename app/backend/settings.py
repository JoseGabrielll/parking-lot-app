import os
from dotenv import load_dotenv

load_dotenv(override=True)

class AppSettings():
    def __init__(self, 
                 db_server: str = os.getenv("DATABASE_URL"),
                 secret_key: str = os.getenv("SECRET_KEY"),
                 algorithm: str = os.getenv("ALGORITHM"),
                 access_token_expire_minutes: str = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) -> None:
        self.DB_SERVER = db_server
        self.SECRET_KEY = secret_key
        self.ALGORITHM = algorithm
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(access_token_expire_minutes)
