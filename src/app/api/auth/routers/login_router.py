from typing import Annotated, Any

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.app.api.auth import schemas
from src.app.api.auth.actions.auth import authenticate_user
from src.app.api.auth.hasher import hasher
from src.app.api.auth.utils import send_reset_password_email
from src.app.api.deps import CurrentUser, SessionDep
from src.app.core import auth_settings
from src.app.core.security import create_access_token
from src.app.db.dals import UserDAL

router = APIRouter()


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> schemas.Token:
    user = await authenticate_user(
        email=credentials.username,
        password=credentials.password,
        session=session,
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = await create_access_token(
        data={"sub": user.email}, expire_time=auth_settings.ACCESS_TOKEN_EXPIRE
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.post("/test-token", response_model=schemas.UserRead)
async def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery", response_model=schemas.Msg)
async def recover_password(
    session: SessionDep,
    email: str = Form(...),
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
    await send_reset_password_email(
        email_to=user.email, token=password_reset_token, username=user.username
    )
    return schemas.Msg(msg="Password recovery email sent")


@router.post("/password-reset", response_model=schemas.Msg)
async def reset_password(
    user: CurrentUser,
    session: SessionDep,
    new_password: str = Form(...),
) -> schemas.Msg | HTTPException:
    user = await UserDAL(session).update_user(
        user.id,
        hashed_password=hasher.get_password_hash(new_password),
    )
    if user is not None:
        return schemas.Msg(msg="Password updated successfully")
    return HTTPException(status_code=400, detail="Something went wrong.")
