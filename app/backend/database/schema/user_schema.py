from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class UserPayload(BaseModel):
    username: str
    password: str
    email: str


class UserSchema(BaseModel):
    """Base user schema

    Args:
        BaseModel (User): base user
    """
    id: Optional[int]
    email: Optional[str]
    username: Optional[str]
    is_active: bool
    role: Optional[str]

    created_date: Optional[datetime]
    created_by: Optional[str]
    updated_date: Optional[datetime]
    updated_by: Optional[str]

    model_config = {
        'from_attributes': True
    }
