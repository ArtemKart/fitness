from typing import Any

from fastapi import APIRouter

import app.api.auth.schemas as schemas
from app.api.auth.actions.users import create_user
from app.api.deps import SessionDep

router = APIRouter()


@router.post("/", response_model=schemas.UserRead)
async def register(
    data: schemas.UserCreate, session: SessionDep
) -> Any:
    new_user: schemas.UserRead = await create_user(data, session)
    return new_user
