from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.hasher import hasher
from app.auth.schemas import UserCreate, UserRead
from app.db import UserDAL


async def create_user(data: UserCreate, session: AsyncSession):
    async with session.begin():
        user = await UserDAL(session).create_user(
            username=data.username,
            email=data.email,
            name=data.name,
            hashed_password=hasher.get_password_hash(data.password),
        )
        if user is not None:
            return UserRead(
                email=user.email,
                name=user.name,
            )
        raise HTTPException(status_code=503, detail=f"User has not beed created")
