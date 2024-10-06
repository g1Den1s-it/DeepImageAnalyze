import datetime
from typing import Optional

from pydantic import BaseModel


class ReportsListSchema(BaseModel):
    id: Optional[int] = None
    title: str
    image: Optional[str] = None
    report: Optional[str] = None
    create_at: Optional[datetime.datetime] = None

