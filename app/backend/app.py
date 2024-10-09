import os
from fastapi import Depends, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.backend.database.database import connect_db, get_database_session, upgrade_database
from app.backend.settings import AppSettings


def register_route(application: FastAPI):
    """It registers all routes used by the application

    Args:
        application (FastAPI): main application
    """
    from app.backend.route.frontend_route import frontend_router
    from app.backend.route.user_route import user_router
    from app.backend.route.auth_route import token_router

    application.include_router(frontend_router)
    application.include_router(user_router, dependencies = [Depends(get_database_session)])
    application.include_router(token_router, dependencies = [Depends(get_database_session)])

    angular_dist_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist', 'frontend', 'browser')
    application.mount("/", StaticFiles(directory=angular_dist_dir, html=True), name="browser")


def create_app(app_settings = AppSettings()) -> FastAPI:
    """It creates the main application

    Args:
        config (class, optional): Config class. Defaults to AppConfig().
    """
    application = FastAPI(title="PyParking", 
                          version="0.0.1", 
                          description="PyParking")
    async_engine = connect_db(app_settings.DB_SERVER)
    upgrade_database(async_engine)
    register_route(application)
    register_422_exception_handler(application)

    return application


def register_422_exception_handler(application: FastAPI):
    """It is used to customize the FastAPI 422 status code

    Args:
        application (FastAPI): main application

    Returns:
        None: None
    """
    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": "Error on request body. Please check the submitted data and correct the issues."})
        )


