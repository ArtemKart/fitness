import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")
    POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
    JWT_SECRET: str = os.environ.get("JWT_SECRET")


settings = Settings()
