from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from app.auth.actions.auth import get_current_user_from_token
from app.db.models import User
from app.pages.template import templates

router_main = APIRouter(tags=["Main"])


@router_main.get("/main", response_class=HTMLResponse)
async def get_base_page(
    request: Request, current_user: User = Depends(get_current_user_from_token)
):
    is_authenticated = True if current_user else False
    return templates.TemplateResponse(
        "main_page.html", {"request": request, "is_authenticated": is_authenticated}
    )
