from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.report.schemas import ReportsListSchema
from src.auth.models import User
from src.report.models import Report


async def get_all_user_reports(user_id: int, db: AsyncSession) -> list[ReportsListSchema]:
    try:
        query = select(Report).where(Report.user_id == user_id)

        query_response = await db.execute(query)

        reports = query_response.scalars().all()

        report_list = [ReportsListSchema.parse_obj({
            "id": report.id,
            "title": report.title,
            "image": report.image,
            "report": report.report,
            "create_at": report.create_at
        }) for report in reports]
        return report_list
    except Exception as e:
        raise e


async def create_report(user_id: int, data: ReportsListSchema, db: AsyncSession) -> Report:
    try:
        report = Report(
            title=data.title,
            image=data.image,
            report=data.report,
            user_id=user_id,
            create_at=data.create_at
        )

        db.add(report)
        await db.commit()

        return report

    except Exception as e:
        raise e


async def get_current_report(user_id: int, report_id: int, db: AsyncSession) -> Report:
    try:
        query = select(Report).where(Report.user_id == user_id, Report.id == report_id)
        execute = await db.execute(query)

        report = execute.scalars().first()

        return report

    except Exception as e:
        raise e
