from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.db.models import User
from src.app.db.session import get_async_session


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def create_user(
        self,
        username: str,
        email: str,
        name: str,
        hashed_password: str,
    ) -> User:
        new_user = User(
            username=username,
            email=email,
            name=name,
            hashed_password=hashed_password,
        )
        self.session.add(new_user)
        await self.session.flush()
        return new_user

    async def update_user(self, user_id: int, **kwargs):
        query = (
            update(User)
            .where(User.id == user_id)
            .values(kwargs)
            .returning(User)
        )
        result = await self.session.execute(query)
        if res := result.first():
            return res[0]

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        if res := result.first():
            return res[0]
