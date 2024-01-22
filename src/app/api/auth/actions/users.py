from fastapi import HTTPException

from app.api.auth.actions.auth import get_user_by_email
from app.api.auth.hasher import hasher
from app.api.auth.schemas import UserCreate, UserRead
from app.api.auth.utils import send_new_account_email
from app.db.dals import UserDAL
from app.api.deps import SessionDep


async def create_user(
    data: UserCreate, session: SessionDep
) -> UserRead | HTTPException:
    async with session.begin():
        user = await get_user_by_email(data.email, session)
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
            await send_new_account_email(email_to=user.email, username=user.username)
            return UserRead(
                email=user.email,
                name=user.name,
            )
        raise HTTPException(status_code=503, detail=f"User has not beed created.")
