from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.utils import authenticate_user, create_access_token, get_current_user_from_token
from api.config import auth_settings
from api.db.models import User
from api.auth.schemas import Token
from api.db.session import get_async_session

auth_router = APIRouter(
    prefix="/login",
    tags=["Auth"],
)
# register_router = fastapi_user.get_register_router(UserRead, UserCreate)


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    credentials: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> Token:
    user: User | None = await authenticate_user(
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


@auth_router.get("/test_auth_endpoint")
async def endpoint_jwt(current_user: User = Depends(get_current_user_from_token)):
    return {"Success": True, "current_user": current_user}
