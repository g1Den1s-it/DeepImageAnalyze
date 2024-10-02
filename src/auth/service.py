from datetime import datetime, timedelta
from jose import jwt

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.auth.models import User
from src.auth.schemas import UserInputSchema, TokenSchema
from src.auth.utils import create_password_hash
from src.auth.config import jwt_token_config


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


async def create_user_jwt_token(user: UserInputSchema) -> TokenSchema:
    to_encode = {"email": user.email, "type": "access"}
    expire = datetime.utcnow() + timedelta(minutes=jwt_token_config.ACCESS_TOKEN_EXPIRE_MIN)
    to_encode['expire'] = expire.strftime("%Y-%m-%d %H:%M:%S")

    access_token = jwt.encode(to_encode, jwt_token_config.JWT_SECRET, jwt_token_config.JWT_ALG)

    refresh_token_payload = {
        "type": "refresh",
        "sub": user.email,
        "exp": datetime.utcnow() + timedelta(days=jwt_token_config.REFRESH_TOKEN_EXPIRE_DAYS),
    }
    refresh_token = jwt.encode(refresh_token_payload, jwt_token_config.JWT_SECRET, jwt_token_config.JWT_ALG)

    token = TokenSchema(access_token=access_token, refresh_token=refresh_token)

    return token


async def get_current_user(user: UserInputSchema, db: AsyncSession) -> UserInputSchema | None:
    try:
        query = select(User).where(User.email == user.email)
        res = await db.execute(query)

        user_obj = res.scalars().first()
        user = UserInputSchema.parse_obj({"id": user_obj.id,
                                          "username": user_obj.username,
                                          "email": user_obj.email,
                                          "password": user_obj.password_hash})

        return user

    except Exception as e:
        return


async def create_new_access_token(user_data: dict) -> str:
    payload = user_data
    expire = datetime.utcnow() + timedelta(minutes=jwt_token_config.ACCESS_TOKEN_EXPIRE_MIN)
    payload['expire'] = expire.strftime("%Y-%m-%d %H:%M:%S")

    access_token = jwt.encode(payload, jwt_token_config.JWT_SECRET, jwt_token_config.JWT_ALG)

    return access_token
