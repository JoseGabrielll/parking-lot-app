from fastapi import APIRouter, Depends, Request

from app.backend.database.database import get_database

user_router = APIRouter(prefix="/api/user")

@user_router.get("/", tags=['User'])
async def get_users(request: Request, database = Depends(get_database)):
    return {"Hello": "World"} 