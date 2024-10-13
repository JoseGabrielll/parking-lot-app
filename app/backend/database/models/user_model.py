from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import Field, Column, Integer, SQLModel, Sequence, func

class UserRoles(str, Enum):
    EMPLOYEE = "EMPLOYEE"
    ADMIN = "ADMIN"

class User(SQLModel, table=True):
    """ User model/schema """
    __tablename__ = 'user'

    id: Optional[int] = Field(sa_column=Column(Integer(), Sequence('user_id_seq'), primary_key=True))
    email: Optional[str] = Field(max_length=256, nullable=False, index=True, sa_column_kwargs={"unique": True})
    username: Optional[str] = Field(max_length=255, nullable=False, index=True, sa_column_kwargs={"unique": True})
    password: Optional[str] = Field(max_length=255, nullable=False)
    is_active: bool = Field(default=True)
    role: Optional[str] = Field(max_length=255, nullable=False, default=UserRoles.EMPLOYEE.value)

    created_date: Optional[datetime] = Field(default=datetime.now(), sa_column_kwargs={"server_default": func.now()}, nullable=True)
    created_by: Optional[str] = Field(max_length=255, nullable=True)
    updated_date: Optional[datetime] = Field(default=datetime.now(), nullable=True)
    updated_by: Optional[str] = Field(max_length=255, nullable=True)
