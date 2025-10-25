# python
from contextlib import contextmanager

# fastapi
from fastapi import FastAPI

def create_app() -> FastAPI:

    @contextmanager
    async def app_lifespan(app: FastAPI):
        # await load_app_settings() # 1. Load app settings
        # await setup_metadata(app) # 2. Update app metadata
        
        yield
    app = FastAPI(lifespan=app_lifespan)
    return app