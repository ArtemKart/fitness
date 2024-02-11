from datetime import timedelta, datetime

from jose import jwt

from src.app.core.config import auth_settings


async def create_access_token(
    data: dict,
    expire_time: int
):
    to_encode = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=expire_time)
    to_encode.update({"exp": expire_time})
    return jwt.encode(
        to_encode,
        auth_settings.JWT_SECRET_KEY,
        auth_settings.ENCODING_ALGORITHM,
    )
