from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import app.auth.schemas as schemas
from app.auth.actions.users import create_user
from app.db.session import get_async_session

router = APIRouter()


@router.post("/", response_model=schemas.UserRead)
async def register(
    data: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)
) -> Any:
    new_user: schemas.UserRead = await create_user(data, session)
    return new_user
