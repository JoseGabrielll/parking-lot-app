from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.backend.database.models.user_model import User
from app.backend.database.database import engine

class UserDAO:

    @staticmethod
    async def create_user(user: User) -> User:
        async with AsyncSession(engine) as session:
            async with session.begin(): # Is necessary once the object will be changed in db
                session.add(user)
            await session.refresh(user)

        return user.model_dump(exclude={"password"})

    @staticmethod
    async def get_user_by_field(attribute: str, value: Any) -> User | None:
        async with AsyncSession(engine) as session:
            statement = select(User).where(getattr(User, attribute) == value)
            result = await session.execute(statement)
            return result.scalars().first()
