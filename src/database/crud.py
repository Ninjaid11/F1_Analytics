from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
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

async def get_reports(db: AsyncSession, skip: int = 0, limit: int = 100):
    try:
        stmt = (
            select(Report)
            .order_by(Report.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        reports = result.scalars().all()
        return reports
    except SQLAlchemyError as e:
        print(f"db error - get_reports: {e}")
        return []

async def delete_report(db: AsyncSession, report_id: int):
    try:
        report = await db.get(Report, report_id)
        if report:
            await db.delete(report)
            await db.commit()
            return True
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"db error - delete_report: {e}")
        return False