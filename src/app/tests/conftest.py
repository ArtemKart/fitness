from typing import Generator, AsyncGenerator, Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import TEST_DATABASE_URL
from app.db.session import async_session_maker, get_async_session
from src.app.tests.utils import get_test_user_token_headers
from src.main import app


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    app.dependency_overrides[get_async_session] = _test_async_session
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def test_user_token_headers(client: TestClient) -> dict[str, str]:
    return get_test_user_token_headers(client)

@pytest.fixture
async def _test_async_session() -> Generator:
    try:
        test_engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)
        test_async_session = async_session_maker(test_engine, expire_on_commit=False)
        yield test_async_session()
    finally:
        pass
