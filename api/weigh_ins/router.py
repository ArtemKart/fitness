import datetime

from fastapi import APIRouter, Depends, Request
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.base_config import current_user
from api.auth.models import User
from api.db.session import get_async_session
from api.pages.router import templates
from api.weigh_ins.models import Weigh
from api.weigh_ins.schemas import WeighCreate
from api.weigh_ins.service import get_history_weighs_plot

import plotly.io as pio

weigh_router = APIRouter(
    prefix="/weigh",
    tags=["Weigh"],
)


@weigh_router.post("/", response_model=dict[str, str])
async def add_weigh_ins(
    new_weigh: WeighCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    stmt = insert(Weigh).values(**new_weigh.model_dump() | {"user_id": user.id})
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@weigh_router.get("/history")
async def get_weigh_history(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Weigh.weigh, Weigh.datetime).where(Weigh.user_id == user.id)
    result = await session.execute(query)
    result_dict: dict[float | int, datetime.datetime] = {
        # row._mapping.weigh: row._mapping.datetime.date() for row in result
    }
    return result_dict


@weigh_router.get("/plot")
async def get_weigh_plot(
    request: Request,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Weigh.weigh, Weigh.datetime).where(Weigh.user_id == user.id)
    result = await session.execute(query)
    result_list = [row for row in result.all()]
    fig = await get_history_weighs_plot(result_list)
    plotly_styles = pio.to_html(fig, full_html=False, include_plotlyjs=False)
    plotly_script = pio.to_html(fig, full_html=False, include_plotlyjs=True)

    return templates.TemplateResponse("plot.html", {"request": request, "plotly_styles": plotly_styles, "plotly_script": plotly_script})
