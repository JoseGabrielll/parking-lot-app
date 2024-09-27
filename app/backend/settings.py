from dotenv import load_dotenv
import os

class AppSettings():
    def __init__(self) -> None:
        load_dotenv()
        self.DB_SERVER = "sqlite+aiosqlite:///pyparking.db"
        # self.DB_SERVER = os.getenv("DATABASE_URL")
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


class AppTestConfig(AppSettings):
    def __init__(self) -> None:
        super().__init__()
        self.DB_SERVER = "sqlite+aiosqlite:///:memory:"

# test_config = AppTestConfig()
app_settings = AppSettings()