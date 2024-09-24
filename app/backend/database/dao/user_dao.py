from sqlmodel import Session, select
from app.backend.database.models.user_model import User
from app.backend.database.database import engine


class UserDAO:

    @staticmethod
    def create_user(user: User) -> User:
        with Session(engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)
        
        return user.model_dump(exclude={"password"})
    
    @staticmethod
    def get_user_by_id(id: int) -> User | None:
        with Session(engine) as session:
            statement = select(User).where(User.id == id)
            return session.exec(statement).first()