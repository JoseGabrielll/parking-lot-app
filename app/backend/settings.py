from dotenv import load_dotenv
import os

class AppSettings():
    load_dotenv(override=True)
    def __init__(self, db_server: str = os.getenv("DATABASE_URL")) -> None:
        self.DB_SERVER = db_server
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
