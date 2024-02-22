import uvicorn
from fastapi import FastAPI
from starlette.templating import Jinja2Templates

from src.app.api.auth.routers import auth_router
from src.app.api.receipts.router import receipt_router
from src.app.api.weight_ins.router import weight_router
from src.app.core.config import APP_PATH

app = FastAPI()

templates = Jinja2Templates(directory=APP_PATH / "templates")

app.include_router(auth_router)
app.include_router(weight_router)
app.include_router(receipt_router)

# Keep it for debugging
if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
