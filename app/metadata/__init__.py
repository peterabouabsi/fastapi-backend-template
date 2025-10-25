from fastapi import FastAPI

from config.settings import get_app_settings

async def setup_metadata(app: FastAPI):
    app_settings = get_app_settings()

    # Update app metadata dynamically
    app.title = app_settings.APP_TITLE if app_settings.APP_TITLE else "FastAPI"
    app.description = app_settings.APP_DESCRIPTION if app_settings.APP_DESCRIPTION else "FastAPI API"
    app.version = app_settings.APP_VERSION if app_settings.APP_VERSION else "1.0.0"
    app.openapi_url = app_settings.APP_OPENAPI_URL if app_settings.APP_OPENAPI_URL else "/openapi.json"
    app.docs_url = app_settings.APP_DOCS_URL if app_settings.APP_DOCS_URL else "/docs"
    app.redoc_url = app_settings.APP_REDOC_URL if app_settings.APP_REDOC_URL else "/redoc"