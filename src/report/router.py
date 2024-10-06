from fastapi import APIRouter, status, Depends, Form, UploadFile, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db_session
from src.report.dependencies import get_list_user_reports, create_user_report
from src.report.schemas import ReportsListSchema

report_router = APIRouter(prefix="/api")



@report_router.get("/reports/",
                   status_code=status.HTTP_200_OK,
                   response_model=list[ReportsListSchema])
async def get_list_reports(report_list: list[dict] = Depends(get_list_user_reports)):
    return report_list


@report_router.post("/reports/create/",
                    status_code=status.HTTP_201_CREATED,
                    response_model=ReportsListSchema)
async def create_report(image: UploadFile,
                        title: str = Form(...),
                        authorization: str = Header(None),
                        db: AsyncSession = Depends(get_db_session)):
    return await create_user_report(ReportsListSchema(title=title), image, authorization, db)

