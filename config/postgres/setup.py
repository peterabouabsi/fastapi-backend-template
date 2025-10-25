from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.settings import get_app_settings, AppSettings

engine = None
AsyncSessionLocal = None
Base = declarative_base()

async def setup_pg_connection():
    """
    Set up the Postgres database connection.
    """
    global engine, AsyncSessionLocal

    app_settings: AppSettings = await get_app_settings()

    DB_USERNAME_PG: str = app_settings.DB_USERNAME_PG
    DB_PASS_PG: str = app_settings.DB_PASS_PG
    DB_HOST_PG: str = app_settings.DB_HOST_PG
    DB_PORT_PG: int = app_settings.DB_PORT_PG
    DB_NAME_PG: str = app_settings.AWS_RDS__DB_NAME_PG
    
    DATABASE_URL_PG = f"postgresql+asyncpg://{DB_USERNAME_PG}:{DB_PASS_PG}@{DB_HOST_PG}:{DB_PORT_PG}/{DB_NAME_PG}"
    
    engine = create_async_engine(DATABASE_URL_PG, echo=False)
    AsyncSessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    print("[INFO] Conencted to Database")
    
    # Create the tables
    # from services.client import model
    # async with engine.begin() as conn:
    #     await conn.run_sync(model.Base.metadata.create_all)
