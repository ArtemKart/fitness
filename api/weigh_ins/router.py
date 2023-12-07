from fastapi import APIRouter, Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.session import get_async_session
from api.weigh_ins.models import Weigh
from api.weigh_ins.schemas import WeighCreate

weigh_router = APIRouter(
    prefix="/weigh",
    tags=["Weigh"],
)

@weigh_router.post("/", response_model=dict[str, str])
async def add_weigh_ins(
    new_weigh: WeighCreate,
    session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(Weigh).values(**new_weigh.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
