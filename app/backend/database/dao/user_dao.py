from typing import Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.database.models.user_model import User
from app.backend.database.database import get_database_session

class UserDAO:

    @staticmethod
    async def create_user(database: AsyncSession, user: User) -> User:
        async with database.begin(): # Is necessary once the object will be changed in db
            database.add(user)
        await database.refresh(user)

        return user.model_dump(exclude={"password"})

    @staticmethod
    async def get_user_by_field(database: AsyncSession, attribute: str, value: Any) -> User | None:
        statement = select(User).where(getattr(User, attribute) == value).limit(1)
        result = await database.execute(statement)
        return result.scalars().first()
