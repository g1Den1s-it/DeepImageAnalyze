from typing import Mapping

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import service
from src.auth.exceptions import UserNotCreated, UserNotFound, WrongPassword
from src.auth.schemas import UserInputSchema, TokenSchema
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
