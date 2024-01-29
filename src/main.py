import uvicorn
from fastapi import FastAPI
from starlette.templating import Jinja2Templates

from app.api.auth.routers import auth_router
from app.api.weight_ins.router import weight_router
from app.core.config import APP_PATH

app = FastAPI()

# app.mount(
#     "../frontend/static", StaticFiles(directory=APP_PATH / "static"), name="static"
# )
templates = Jinja2Templates(directory=APP_PATH / "templates")

app.include_router(auth_router)
app.include_router(weight_router)


# Keep it for debugging
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
