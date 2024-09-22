from datetime import datetime
from typing import Optional
from sqlmodel import Field, Column, Integer, SQLModel, Sequence, func


class User(SQLModel, table=True):
    """ User model/schema """
    __tablename__ = 'user'

    id: Optional[int] = Field(sa_column=Column(Integer(), Sequence('user_id_seq'), primary_key=True))
    name: Optional[str] = Field(max_length=256, nullable=True)
    email: Optional[str] = Field(max_length=256, index=True, nullable=True)
    is_active: bool = Field(default=True)

    created_date: Optional[datetime] = Field(default=datetime.now(), sa_column_kwargs={"server_default": func.now()}, nullable=True)
    created_by: Optional[str] = Field(max_length=255, nullable=True)
    updated_date: Optional[datetime] = Field(default=datetime.now(), nullable=True)
    updated_by: Optional[str] = Field(max_length=255, nullable=True)
