from fastapi import Depends, status, HTTPException
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.base_config import oauth2_scheme
from app.auth.hasher import hasher
from app.core.config import auth_settings
from app.db import UserDAL, User, get_async_session


async def _get_user_by_email_for_auth(
    email: str, session: AsyncSession = Depends(get_async_session)
) -> User | None:
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_email(email)


async def authenticate_user(
    email: str, password: str, session: AsyncSession
) -> User | None:
    user = await _get_user_by_email_for_auth(email=email, session=session)
    if user is not None and hasher.verify_password(password, user.hashed_password):
        return user
    return None


async def get_current_user_from_token(
    session: AsyncSession = Depends(get_async_session),
    token: str = Depends(oauth2_scheme),
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
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_email_for_auth(email=email, session=session)
    if user is not None:
        return user
    raise credentials_exception
