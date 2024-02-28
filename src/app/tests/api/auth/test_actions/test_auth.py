import pytest
from sqlalchemy import insert, select

from app.api.auth.actions.auth import get_user_by_email
from src.app.db.models import User
from conftest import async_session_maker
from utils import super_user


@pytest.mark.parametrize(
    "test_user_email, is_exist_user",
    [
        pytest.param(super_user.username, True, id="Existing user"),
        pytest.param("non existing username", False, id="Non existing user"),
    ],
)
async def test_get_user_by_email(
    test_user_email: str,
    is_exist_user: bool,
) -> None:
    async with async_session_maker() as session:
        user = await get_user_by_email(email=test_user_email, session=session)
        if is_exist_user:
            assert test_user_email == user.email
        else:
            assert user is None


async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(User).values(
            id=1,
            username="test",
            email="test@test.com",
            name="test",
            is_active=True,
            hashed_password="testpass",
        )
        await session.execute(stmt)
        await session.commit()

        query = select(User)
        result = await session.execute(query)
        print(result.all())
