from .setup import Base, AsyncSessionLocal

async def get_postgres_db():
    """
    Manage DB Sessions
    """
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()