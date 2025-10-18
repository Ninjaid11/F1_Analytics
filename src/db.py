from typing import AsyncIterator
import contextlib
from src.database.models import Base

from requests import session
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncConnection,
    AsyncSession,
    AsyncEngine,
)

class DatabaseSessionManager:
    def __init__(self):
        self._sessionmaker: async_sessionmaker | None = None
        self._engine: AsyncEngine | None = None


    def init(self, db_url: str):
        self._engine = create_async_engine(db_url)
        self._sessionmaker = async_sessionmaker(
            autocommit=False,
            expire_on_commit=False,
            bind=self._engine
        )


    async def init_tables(self):
        if self._engine is None:
            raise Exception("Engine не инициализирован")
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None


    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()

        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager()

async def get_db_session():
    async with sessionmanager.session() as session:
        yield session