from fastapi import APIRouter, status, Depends

from src.report.dependencies import get_list_user_reports
from src.report.schemas import ReportsListSchema

report_router = APIRouter(prefix="/api")



@report_router.get("/reports/",
                   status_code=status.HTTP_200_OK,
                   response_model=list[ReportsListSchema])
async def get_list_reports(report_list: list[dict] = Depends(get_list_user_reports)):
    return report_list
