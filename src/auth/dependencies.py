from datetime import datetime
from typing import Mapping

from fastapi import Depends, Header
from jose import jwt

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import service
from src.auth.config import jwt_token_config
from src.auth.exceptions import UserNotCreated, UserNotFound, WrongPassword, UnauthorizedUser, InvalidToken, \
    ExpiredToken, TypeToken
from src.auth.schemas import UserInputSchema
from src.auth.utils import verify_password
from src.database import get_db_session


async def create_user(user: UserInputSchema, db: AsyncSession = Depends(get_db_session)) -> Mapping:
    user = await service.create_user_object(user, db)
    if not user:
        raise UserNotCreated()

    return user


async def get_user(user: UserInputSchema, db: AsyncSession = Depends(get_db_session)) -> UserInputSchema:
    password: str = user.password
    user = await service.get_current_user(user, db)

    if not user:
        raise UserNotFound()

    if not verify_password(password, user.password):
        raise WrongPassword()

    return user


async def get_user_data_refresh_token(token: str) -> str:
    try:
        payload: dict = jwt.decode(token, jwt_token_config.JWT_SECRET, jwt_token_config.JWT_ALG)

        if payload.get("type") != "refresh":
            raise TypeToken()

        if datetime.fromtimestamp(payload.get("exp")) < datetime.utcnow():
            raise ExpiredToken()

        return payload["sub"]

    except:
        raise InvalidToken()


async def get_new_access(authorization: str = Header(None)) -> str:
    if not authorization:
        raise UnauthorizedUser()

    if not authorization.startswith("Bearer "):
        raise InvalidToken()

    refresh_token = authorization[len("Bearer "):]
    user_data = await get_user_data_refresh_token(refresh_token)

    access_token = await service.create_new_access_token({"sub": user_data})

    return access_token
