from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.db.session import get_async_session


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

    async def get_user_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        user = result.fetchone()
        return user[0] if user is not None else None
