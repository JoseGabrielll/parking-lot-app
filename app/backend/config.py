from dotenv import load_dotenv
import os

class AppConfig():
    def __init__(self) -> None:
        # self.DB_SERVER = "sqlite:///pyparking.db"
        self.DB_SERVER = os.getenv("DATABASE_URL")
        # os.environ.get("KEY")


class AppTestConfig(AppConfig):
    def __init__(self) -> None:
        super().__init__()
        self.DB_SERVER = "sqlite:///:memory:"

# test_config = AppTestConfig()