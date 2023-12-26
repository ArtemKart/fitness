import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.auth.routers import auth_router
from app.core.config import APP_PATH

app = FastAPI()

app.mount(
    "../frontend/static", StaticFiles(directory=APP_PATH / "static"), name="static"
)
templates = Jinja2Templates(directory=APP_PATH / "templates")

app.include_router(auth_router)


# Keep it for debugging
if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
