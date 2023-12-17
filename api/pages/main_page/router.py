from fastapi import APIRouter, Request, Depends

from fastapi.responses import HTMLResponse

from api.pages.template import templates
from api.auth.utils import get_current_user_from_token
from api.db.models import User

router_main = APIRouter(tags=["Main"])


@router_main.get("/main", response_class=HTMLResponse)
async def get_base_page(
    request: Request,
    current_user: User = Depends(get_current_user_from_token)
):
    is_authenticated = True if current_user else False
    return templates.TemplateResponse("main_page.html", {"request": request, "is_authenticated": is_authenticated})
