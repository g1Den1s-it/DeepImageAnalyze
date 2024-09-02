import contextlib
import os
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncConnection, AsyncSession
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

SQL_DATABASE_URL = ('postgresql+asyncpg://{}:{}@{}:{}/{}'
                    .format(os.getenv("DB_USER"),
                            os.getenv("DB_PASSWORD"),
                            os.getenv("DB_HOST"),
                            os.getenv("DB_PORT"),
                            os.getenv("DB_NAME")))

Base = declarative_base()


class DBSessionManager:
    def __init__(self):
        self.__engine = create_async_engine(SQL_DATABASE_URL)
        self.__session_maker = async_sessionmaker(self.__engine, expire_on_commit=False)

    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if not self.__engine:
            raise Exception("SessionManager is not initialized")

        async with self.__engine.begin() as conn:
            try:
                yield conn
            except Exception:
                await conn.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if not self.__session_maker:
            raise Exception("SessionManager is not initialized")

        session = self.__session_maker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


session_manager = DBSessionManager()


async def get_db_session():
    async with session_manager.session() as session:
        yield session
