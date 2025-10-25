from fastapi import FastAPI

from config.settings import get_app_settings

from .create import create_api_router

def setup_routes(app: FastAPI):
    api_router = create_api_router()
    app.include_router(router=api_router)
    
    @app.get("/health", tags=['Health Check'])
    async def _():
        app_settings = get_app_settings()
        return {"message": f"{app_settings.APP_TITLE} API is running!"}