import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

APP_PATH = Path(__file__).parent.parent


class AppSettings(BaseSettings):
    PROJECT_NAME: str = "Fitness App"
    PROJECT_EMAIL: str = "test@gmail.com"
    SERVER_HOST: str = os.environ.get("SERVER_HOST")
    SERVER_NAME: str = os.environ.get("SERVER_NAME")


class DbSettings(BaseSettings):
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")
    POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")


class AuthSettings(BaseSettings):
    ACCESS_TOKEN_EXPIRE: int = os.environ.get("ACCESS_TOKEN_EXPIRE", default=30)
    RESET_PASS_TOKEN_EXPIRE: int = os.environ.get("RESET_PASS_TOKEN_EXPIRE", default=30)
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY", default="qwerty12345")
    ENCODING_ALGORITHM: str = os.environ.get("ENCODING_ALGORITHM", default="HS256")


class StmpSettings(BaseSettings):
    STMP_HOST: str = os.environ.get("STMP_HOST")
    STMP_PORT: int = os.environ.get("STMP_PORT")
    STMP_USER: str = os.environ.get("STMP_USER")
    STMP_PASSWORD: str = os.environ.get("STMP_PASSWORD")


class Paths(BaseSettings):
    EMAIL_TEMPLATES_PATH: Path = APP_PATH / "email-templates" / "build"


TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    default="postgresql+asyncpg://postgres_test:postgres_test@0.0.0.0:5433/postgres_test",
)

app_settings = AppSettings()
db_settings = DbSettings()
auth_settings = AuthSettings()
paths = Paths()
stmp_settings = StmpSettings()
