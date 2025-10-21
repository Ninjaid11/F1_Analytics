from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.database.models import Report

async def create_report(db: AsyncSession, prompt: str, response: str):
    try:
        new_report = Report(prompt=prompt, response=response)
        db.add(new_report)
        await db.commit()
        await db.refresh(new_report)
        return new_report
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"db error - create_report: {e} ")
        return None