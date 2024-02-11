from typing import Annotated

from fastapi import HTTPException, status, Depends
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.auth.base_config import oauth2_scheme
from src.app.api.auth.hasher import hasher
from src.app.core.config import auth_settings
from src.app.db.dals import UserDAL
from src.app.db.models import User
from src.app.db.session import get_async_session


async def get_user_by_email(
    email: str, session: Annotated[AsyncSession, Depends(get_async_session)]
) -> User | None:
    user_dal = UserDAL(session)
    return await user_dal.get_user_by_email(email)


async def authenticate_user(
    email: str,
    password: str,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> User | None:
    user = await get_user_by_email(email=email, session=session)
    if user is not None and hasher.verify_password(
        password, user.hashed_password
    ):
        return user
    return None


async def get_current_user_from_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> User | None:
    if token is None:
        return None
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token,
            auth_settings.JWT_SECRET_KEY,
            algorithms=[auth_settings.ENCODING_ALGORITHM],
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except (jwt.JWTError, ValidationError):
        raise credentials_exception
    user = await get_user_by_email(email=email, session=session)
    if user is not None:
        return user
    raise credentials_exception
