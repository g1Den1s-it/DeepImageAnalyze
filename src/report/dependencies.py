from fastapi import Header, Depends
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.config import jwt_token_config
from src.auth.exceptions import UnauthorizedUser, InvalidToken
from src.auth.models import User
from src.auth.schemas import UserInputSchema
from src.auth.service import get_current_user
from src.database import get_db_session
from src.report import service


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
