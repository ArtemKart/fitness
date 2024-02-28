from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.app.core import db_settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{db_settings.POSTGRES_USER}:"
    f"{db_settings.POSTGRES_PASSWORD}@{db_settings.POSTGRES_HOST}:"
    f"{db_settings.POSTGRES_PORT}/{db_settings.POSTGRES_DB}"
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
