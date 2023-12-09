from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router_pages = APIRouter(prefix="/pages", tags=["Pages"])

templates = Jinja2Templates(directory="api/templates")


@router_pages.get("/main", response_class=HTMLResponse)
def get_base_page(request: Request):
    return templates.TemplateResponse("main_page.html", {"request": request})


@router_pages.get("/search", response_class=HTMLResponse)
def get_search_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})


