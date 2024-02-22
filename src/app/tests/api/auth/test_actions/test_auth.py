from typing import AsyncGenerator

from src.app.api.auth.actions.auth import get_user_by_email
from src.app.tests.utils import super_user
import pytest
import asyncio


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.mark.parametrize(
    "test_user_email, is_exist_user",
    [
        pytest.param(super_user.username, True, id="Existing user"),
        pytest.param("non existing username", False, id="Non existing user"),
    ],
)
@pytest.mark.asyncio
async def test_get_user_by_email(
    _test_async_session: AsyncGenerator,
    test_user_email: str,
    is_exist_user: bool,
) -> None:
    async_session = await _test_async_session.__anext__()
    user = await get_user_by_email(email=test_user_email, session=async_session)
    if is_exist_user:
        assert test_user_email == user.email
    else:
        assert user is None
