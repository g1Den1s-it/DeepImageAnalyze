from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.auth.models import User
from src.auth.schemas import UserInputSchema
from src.auth.utils import create_password_hash


async def create_user_object(user: UserInputSchema, db: AsyncSession) -> User | None:
    try:
        user_data = (await db.scalars(select(User).where(User.email == user.email))).first()
        if user_data:
            return

        user_model = User(
            username=user.username,
            email=user.email,
        )
        user_model.password_hash = create_password_hash(user.password)

        db.add(user_model)
        await db.commit()

        return user_model
    except Exception as e:
        return
