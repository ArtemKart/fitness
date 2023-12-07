from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers

from api.auth.base_config import auth_backend
from api.auth.manager import get_user_manager
from api.auth.models import User
from api.auth.schemas import UserRead, UserCreate
from api.weigh_ins.router import weigh_router

app = FastAPI()


@app.get("/")
async def root():
    return{"message": "HI"}


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(weigh_router)

current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"

