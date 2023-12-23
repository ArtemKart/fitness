from datetime import timedelta, datetime

from jose import jwt

from app.core.config import auth_settings


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
