import datetime

from pydantic import BaseModel


class ReportsListSchema(BaseModel):
    id: int
    title: str
    image: str
    report: str
    create_at: datetime.datetime

