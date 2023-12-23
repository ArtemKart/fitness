import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.auth.routers import auth_router
from app.core.config import APP_PATH

app = FastAPI()

app.mount("/app/static", StaticFiles(directory=APP_PATH / "static"), name="static")

app.include_router(auth_router)


# Keep it for debugging
if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
