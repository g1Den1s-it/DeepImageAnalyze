import asyncio
import os

from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio

from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession


from src.database import get_db_session, Base, DBSessionManager
from src.main import app

load_dotenv()

SQL_DATABASE_URL = ('postgresql+asyncpg://{}:{}@{}:{}/{}'
                    .format(os.getenv("DB_USER"),
                            os.getenv("DB_PASSWORD"),
                            os.getenv("DB_HOST"),
                            os.getenv("DB_PORT"),
                            os.getenv("DB_NAME_TEST")))

session_manager = DBSessionManager(SQL_DATABASE_URL)


async def get_test_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_manager.session() as session:
        yield session


app.dependency_overrides[get_db_session] = get_test_async_session


@pytest_asyncio.fixture()
async def db_setup_teardown():
    print("\n--- Test session started ---")
    async with session_manager.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    print("\n--- Test session finished ---")
    async with session_manager.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as aclient:
        yield aclient
