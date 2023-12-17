from datetime import timedelta, datetime

from jose import jwt, JWTError
from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth.base_config import oauth2_scheme
from api.auth.hasher import hasher
from api.config import auth_settings
from api.db.dals import UserDAL
from api.db.models import User
from api.db.session import get_async_session
from api.auth.schemas import UserCreate, UserRead
from fastapi.responses import RedirectResponse


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


async def create_access_token(
    data: dict,
    expires_delta: timedelta = timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE),
):
    to_encode = data.copy()
    expire_time = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire_time})
    return jwt.encode(
        to_encode,
        auth_settings.JWT_SECRET_KEY,
        auth_settings.ENCODING_ALGORITHM,
    )


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
