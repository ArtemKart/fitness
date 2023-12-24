from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.actions.auth import get_user_by_email
from app.auth.hasher import hasher
from app.auth.schemas import UserCreate, UserRead
from app.db.dals import UserDAL


async def create_user(data: UserCreate, session: AsyncSession):
    async with session.begin():
        user = get_user_by_email(data.email, session)
        if user:
            raise HTTPException(
                status_code=400,
                detail=f"The user with email: {data.email} already exists.",
            )
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
