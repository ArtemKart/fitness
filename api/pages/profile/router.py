from fastapi import APIRouter, Request, Depends

from fastapi.responses import HTMLResponse

from api.auth.utils import get_current_user_from_token
from api.db.models import User
from api.pages.template import templates

router_profile = APIRouter(prefix="", tags=["Profile"])


@router_profile.get("/profile", response_class=HTMLResponse)
async def profile(
    request: Request,
    current_user: User = Depends(get_current_user_from_token),
):
    if current_user:
        print("ZALOGIROVAN")
    return templates.TemplateResponse("base.html", {"request": request})
