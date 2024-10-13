from app.backend.database.dao.user_dao import UserDAO
from app.backend.database.models.user_model import User
from app.backend.service.auth_service import AuthenticationService


async def mock_user(async_session, user: User = User(email="dummy@gmail.com", username="dummy123", password="123456")):
    user.password = AuthenticationService.generate_password_hash(user.password)
    return await UserDAO.create_user(async_session, user)
