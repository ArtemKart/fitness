import pytest

from app.api.auth.actions.auth import get_user_by_email, authenticate_user, get_current_user_from_token
from app.api.auth.hasher import hasher
from conftest import async_session_maker, test_superuser_token_headers
from utils import super_user


@pytest.mark.parametrize(
    "test_user_email, existing_user",
    [
        pytest.param(super_user.email, True, id="Existing user"),
        pytest.param("non existing username", False, id="Non existing user"),
    ],
)
async def test_get_user_by_email(
    test_user_email: str,
    existing_user: bool,
) -> None:
    async with async_session_maker() as session:
        user = await get_user_by_email(email=test_user_email, session=session)
        if existing_user:
            assert test_user_email == user.email
        else:
            assert user is None


@pytest.mark.parametrize(
    "email, password, existing_user",
    [
        pytest.param(super_user.email, super_user.password, True, id="Existing user"),
        pytest.param("non existing username", "dsfsdfsdf", False, id="Non existing user"),
    ],
)
async def test_authenticate_user(email: str, password: str, existing_user: bool) -> None:
    async with async_session_maker() as session:
        user = await authenticate_user(email=email, password=password, session=session)
        if existing_user:
            assert user.email == email
            assert hasher.verify_password(password, user.hashed_password)


async def test_get_current_user_from_token(test_superuser_token_headers) -> None:
    token = test_superuser_token_headers["Authorization"]
    async with async_session_maker() as session:
        await get_current_user_from_token(token=token, session=session)
