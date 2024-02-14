from typing import AsyncGenerator

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.app.core.config import db_settings

SQLALCHEMY_DATABASE_URL = str(
    URL.create(
        drivername="postgresql+asyncpg",
        username=db_settings.POSTGRES_USER,
        password=db_settings.POSTGRES_PASSWORD,
        host=db_settings.POSTGRES_HOST,
        port=db_settings.POSTGRES_PORT,
        database=db_settings.POSTGRES_DB,
    )
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
