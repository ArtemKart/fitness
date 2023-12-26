import datetime

import plotly.io as pio
from fastapi import APIRouter, Depends, Request
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import APP_PATH
from app.db.models import User, Weigh
from app.db.session import get_async_session
from src.main import templates
from app.weigh_ins.schemas import WeighCreate
from app.weigh_ins.service import get_history_weighs_plot

weigh_router = APIRouter(
    prefix="/weigh",
    tags=["Weigh"],
)


@weigh_router.post("/add", response_model=None)
async def add_weigh_ins(
    new_weigh: WeighCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(),
) -> None:
    stmt = insert(Weigh).values(**new_weigh.model_dump() | {"user_id": user.id})
    await session.execute(stmt)
    await session.commit()


@weigh_router.get("/history")
async def get_weigh_history(
    user: User = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Weigh.weigh, Weigh.datetime).where(Weigh.user_id == user.id)
    result = await session.execute(query)
    result_dict: dict[float | int, datetime.date] = {
        row[0]: row[1].date() for row in result
    }
    return result_dict


@weigh_router.get("/plot")
async def get_weigh_plot(
    request: Request,
    user: User = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Weigh.weigh, Weigh.datetime).where(Weigh.user_id == user.id)
    result = await session.execute(query)
    result_list = list(result.all())
    fig = await get_history_weighs_plot(result_list)
    plotly_styles = pio.to_html(fig, full_html=False, include_plotlyjs=False)
    plotly_script = pio.to_html(fig, full_html=False, include_plotlyjs=True)
    return templates.TemplateResponse(
        APP_PATH / "template" / "plot.html",
        {
            "request": request,
            "plotly_styles": plotly_styles,
            "plotly_script": plotly_script,
        },
    )
