import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from src.database.models import Base
from src.config import Settings

settings = Settings()
engine = create_async_engine(settings.DB_URL, echo=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_db())