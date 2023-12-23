from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import app.auth.schemas as schemas
from app.auth.actions.users import create_user
from app.db import get_async_session

router = APIRouter()


@router.post("/", response_model=schemas.UserCreate)
async def register(
    data: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)
):
    new_user: schemas.UserCreate = await create_user(data, session)
    return {"success": True, "created_user": new_user}
