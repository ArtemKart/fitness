from fastapi import APIRouter

from app.api.auth.routers import user_router
from app.api.auth.routers import login_router

auth_router = APIRouter()
auth_router.include_router(login_router.router, prefix="/login", tags=["login"])
auth_router.include_router(user_router.router, prefix="/users", tags=["users"])
