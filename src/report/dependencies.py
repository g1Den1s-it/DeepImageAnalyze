import datetime
import os.path

from fastapi import Header, Depends, File, UploadFile
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.config import jwt_token_config
from src.auth.exceptions import UnauthorizedUser, InvalidToken
from src.auth.models import User
from src.auth.schemas import UserInputSchema
from src.auth.service import get_current_user
from src.config import static_base_config
from src.database import get_db_session
from src.report import service
from src.report.pdf_reporter import PDFReporter
from src.report.schemas import ReportsListSchema


async def get_list_user_reports(authorization: str = Header(None), db: AsyncSession = Depends(get_db_session)):
    if not authorization:
        raise UnauthorizedUser()

    if not authorization.startswith("Bearer "):
        raise InvalidToken()

    token = authorization[len("Bearer "):]
    user = await get_user(token, db)

    list_reports = await service.get_all_user_reports(user.id, db)

    return list_reports


async def get_user(token: str, db: AsyncSession) -> UserInputSchema | None:
    payload: dict = jwt.decode(token, jwt_token_config.JWT_SECRET, jwt_token_config.JWT_ALG)

    user = await get_current_user(UserInputSchema.parse_obj({"email": payload["email"], "password": "dqwdqwdqwq"}), db)

    return user


async def create_user_report(data: ReportsListSchema,
                             image: UploadFile,
                             authorization: str,
                             db: AsyncSession) -> ReportsListSchema:
    if not authorization:
        raise UnauthorizedUser()

    if not authorization.startswith("Bearer "):
        raise InvalidToken()

    pdf_report = PDFReporter(data)

    pdf_report.create_report()
    data.report = pdf_report.save_pdf()

    path = f"{static_base_config.MEDIA_NAME}/images"
    if not os.path.exists(path):
        os.makedirs(path)

    file_path = f"{path}/{image.filename}".replace(" ", "_")

    with open(file_path, "wb") as file:
        file.write(await image.read())

    data.image = file_path

    data.create_at = datetime.datetime.now()

    token = authorization[len("Bearer "):]
    user = await get_user(token, db)

    report = await service.create_report(user.id, data, db)

    return report


async def get_detail_report(report_id: int,
                            authorization: str = Header(None),
                            db: AsyncSession = Depends(get_db_session)) -> ReportsListSchema:
    if not authorization:
        raise UnauthorizedUser()

    if not authorization.startswith("Bearer "):
        raise InvalidToken()

    token = authorization[len("Bearer "):]
    user = await get_user(token, db)

    report = await service.get_current_report(user.id, report_id, db)

    return report
