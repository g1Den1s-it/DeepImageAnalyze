from typing import Mapping

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import service
from src.auth.exceptions import UserNotCreated
from src.auth.schemas import UserInputSchema
from src.database import get_db_session


async def create_user(user: UserInputSchema, db: AsyncSession = Depends(get_db_session)) -> Mapping:
    user = await service.create_user_object(user, db)
    if not user:
        raise UserNotCreated()

    return user
