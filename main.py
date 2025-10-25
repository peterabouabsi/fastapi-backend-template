from fastapi import FastAPI

from app import create_app
from app.exceptions import setup_exception_handlers
from app.middlewares import setup_middlewares
from app.routes import setup_routes

app: FastAPI = create_app()

setup_middlewares(app)
setup_exception_handlers(app)
setup_routes(app)
