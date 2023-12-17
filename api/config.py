import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path

load_dotenv()

API_PATH = Path(__file__).parent


class DbSettings(BaseSettings):
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")
    POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")


class AuthSettings(BaseSettings):
    ACCESS_TOKEN_EXPIRE: int = os.environ.get("ACCESS_TOKEN_EXPIRE", default=30)
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY", default="qwerty12345")
    ENCODING_ALGORITHM: str = os.environ.get("ENCODING_ALGORITHM", default="HS256")


db_settings = DbSettings()
auth_settings = AuthSettings()
