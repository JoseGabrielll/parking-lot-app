from pydantic import BaseModel


class UserPayload(BaseModel):
    username: str
    password: str
    email: str
