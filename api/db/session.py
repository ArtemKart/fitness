from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from api.config import settings


SQLALCHEMY_DATABASE_URL_ALEMBIC = str(
    URL.create(
        drivername="postgresql",
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DB,
    )
)

SQLALCHEMY_DATABASE_URL_USERS = str(
    URL.create(
        drivername="postgresql+asyncpg",
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DB,
    )
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL_USERS)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, autoflush=False,)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
