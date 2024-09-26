from typing import Any
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
    def get_user_by_field(attribute: str, value: Any) -> User | None:        
        with Session(engine) as session:
            statement = select(User).where(getattr(User, attribute) == value)
            return session.exec(statement).first()