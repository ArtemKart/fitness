import datetime
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlalchemy import insert, select

from app.db.models import Weight
import app.api.weight_ins.schemas as weight_schemas
from app.api.deps import CurrentUser, SessionDep

weight_router = APIRouter(
    prefix="/weight",
    tags=["Weight"],
)


@weight_router.post("/add", response_model=Any)
async def add_weight_ins(
    new_weight: weight_schemas.WeightCreate,
    user: CurrentUser,
    session: SessionDep,
) -> weight_schemas.Msg | HTTPException:
    try:
        stmt = insert(Weight).values(**new_weight.model_dump() | {"user_id": user.id})
        await session.execute(stmt)
        await session.commit()
        return weight_schemas.Msg(msg="Data has been successfuly added.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@weight_router.get("/history", response_model=Any)
async def get_weight_history(
    user: CurrentUser,
    session: SessionDep,
) -> weight_schemas.WeightRead | HTTPException:
    try:
        query = select(Weight.weight, Weight.datetime).where(Weight.user_id == user.id)
        result = await session.execute(query)
        result_dict: dict[float | int, datetime.date] = {
            row[1].date(): row[0] for row in result
        }
        result = weight_schemas.WeightRead(
            datetime=result_dict.keys(), values=result_dict.values()
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@weight_router.get("/plot")
async def get_weight_plot(
    user: CurrentUser,
    session: SessionDep,
) -> weight_schemas.WeightRead:
    query = select(Weight.weight, Weight.datetime).where(Weight.user_id == user.id)
    result = await session.execute(query)
    result_dict = {value: date.date() for value, date in result}
    return weight_schemas.WeightRead(values=list(result_dict.keys()), datetime=list(result_dict.values()))
