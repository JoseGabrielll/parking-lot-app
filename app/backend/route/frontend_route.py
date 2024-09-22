import os
from fastapi import APIRouter
from fastapi.responses import FileResponse


frontend_router = APIRouter()

@frontend_router.get("/", include_in_schema=False)
@frontend_router.get("/index.html", include_in_schema=False)
async def serve_frontend():
    angular_dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'dist', 'frontend', 'browser'))
    return FileResponse(os.path.join(angular_dist_dir, "index.html"))