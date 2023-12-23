from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from app.auth.actions.auth import get_current_user_from_token
from app.db import User
from app.pages.template import templates

router_profile = APIRouter(prefix="", tags=["Profile"])


@router_profile.get("/profile", response_class=HTMLResponse)
async def profile(
    request: Request,
    current_user: User = Depends(get_current_user_from_token),
):
    if current_user:
        print("ZALOGIROVAN")
    return templates.TemplateResponse("base.html", {"request": request})
