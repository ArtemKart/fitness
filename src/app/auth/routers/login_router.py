from typing import Any

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import app.auth.schemas as schemas
from app.auth.actions.auth import authenticate_user, get_current_user_from_token
from app.auth.hasher import hasher
from app.auth.utils import send_reset_password_email
from app.core.config import auth_settings
from app.core.security import create_access_token
from app.db.dals import UserDAL
from app.db.models import User
from app.db.session import get_async_session

router = APIRouter()


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    credentials: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> schemas.Token:
    user = await authenticate_user(
        email=credentials.username, password=credentials.password, session=session
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = await create_access_token(
        data={"sub": user.email}, expire_time=auth_settings.ACCESS_TOKEN_EXPIRE
    )
    return {"access_token": access_token, "token_type": "bearer"}  # type: ignore


@router.post("/test-token", response_model=schemas.UserRead)
async def test_token(current_user: User = Depends(get_current_user_from_token)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery", response_model=schemas.Msg)
async def recover_password(
    email: str,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    user = await UserDAL(session).get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"The user with email: {email} does not exist.",
        )
    password_reset_token = await create_access_token(
        data={"sub": email}, expire_time=auth_settings.RESET_PASS_TOKEN_EXPIRE
    )
    await send_reset_password_email(email_to=user.email, token=password_reset_token)
    return {"msg": "Password recovery email sent"}


@router.post("/password-reset", response_model=schemas.Msg)
async def reset_password(
    new_password: str,
    user: User = Depends(get_current_user_from_token),
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    user = await UserDAL(session).update_user(
        user.id,
        hashed_password=hasher.get_password_hash(new_password),
    )
    if user is not None:
        return {"msg": "Password updated successfully"}
    return HTTPException(status_code=400, detail="Something went wrong.")
