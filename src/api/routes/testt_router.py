from fastapi import APIRouter
from sqlalchemy import text

from src.api.dependencies.db import DBSessionDep

router = APIRouter()

@router.get("/")
async def get_db(session: DBSessionDep):
    result = await session.execute(text("SELECT version();"))
    version = result.scalar()  # або result.fetchone()[0]
    return f"faf"