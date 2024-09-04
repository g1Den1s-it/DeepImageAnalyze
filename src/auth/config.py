import os
from dotenv import load_dotenv
from pydantic import BaseConfig, Field

load_dotenv()


class JWTTokenConfig(BaseConfig):
    JWT_ALG: str = "HS256"
    JWT_SECRET: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MIN: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 3


jwt_token_config = JWTTokenConfig()
