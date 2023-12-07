import uvicorn
from fastapi import FastAPI

from api.auth.base_config import auth_backend, fastapi_users
from api.auth.schemas import UserRead, UserCreate
from api.weigh_ins.router import weigh_router

app = FastAPI()


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

# Keep it for debugging
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)