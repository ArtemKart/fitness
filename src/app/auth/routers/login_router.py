from datetime import timedelta
from typing import Any

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import app.auth.schemas as schemas
from app.auth.actions.auth import authenticate_user, get_current_user_from_token
from app.core.config import auth_settings
from app.core.security import create_access_token
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
    access_token_expires = timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE)
    access_token = await create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}  # type: ignore


@router.post("/login/test-token", response_model=schemas.UserRead)
def test_token(current_user: User = Depends(get_current_user_from_token)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}", response_model=schemas.Msg)
def recover_password() -> schemas.Msg:
    """
    Password Recovery
    """
    raise NotImplementedError


@router.post("/reset-password/", response_model=schemas.Msg)
def reset_password() -> schemas.Msg:
    """
    Reset password
    """
    raise NotImplementedError
