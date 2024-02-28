import asyncio
from typing import Generator, Any, AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.pool import NullPool
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.app.db.base_class import meta
from src.app.core import test_db_settings
from src.app.db.session import get_async_session
from src.app.tests.utils import get_test_user_token_headers
from src.main import app


@pytest.fixture(scope="session")
def event_loop(request):  # noqa
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    app.dependency_overrides[get_async_session] = test_async_session  # noqa
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="module")
def test_user_token_headers(client: TestClient) -> dict[str, str]:
    return get_test_user_token_headers(client)


test_db_url = (
    f"postgresql+asyncpg://{test_db_settings.TEST_USER}:"
    f"{test_db_settings.TEST_PASSWORD}@{test_db_settings.TEST_HOST}:"
    f"{test_db_settings.TEST_PORT}/{test_db_settings.TEST_DB}"
)
engine_test = create_async_engine(test_db_url, poolclass=NullPool)
async_session_maker = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
meta.bind = engine_test


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(meta.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(meta.drop_all)
