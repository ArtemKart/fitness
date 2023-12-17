from fastapi import APIRouter, Request

from fastapi.responses import HTMLResponse

from api.pages.template import templates

router_main = APIRouter(tags=["Main"])


@router_main.get("/main", response_class=HTMLResponse)
async def get_base_page(
    request: Request,
):
    return templates.TemplateResponse("main_page.html", {"request": request})
