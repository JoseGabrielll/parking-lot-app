from typing import Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.database.models.user_model import User

class UserDAO:

    @staticmethod
    async def create_user(database: AsyncSession, user: User) -> User:
        database.add(user)
        await database.commit()
        await database.refresh(user)

        return user.model_dump(exclude={"password"})

    @staticmethod
    async def get_user_by_field(database: AsyncSession, attribute: str, value: Any) -> User | None:
        statement = select(User).where(getattr(User, attribute) == value).limit(1)
        result = await database.execute(statement)
        return result.scalars().first()
    
    @staticmethod
    async def get_user_by_username_or_email(database: AsyncSession, user: User) -> User | None:
        statement = select(User).where(User.username == user.username or 
                                       User.email == user.email).limit(1)
        result = await database.execute(statement)
        return result.scalars().first()
