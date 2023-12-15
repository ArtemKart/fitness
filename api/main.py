import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.auth.router import auth_router
from api.config import API_PATH
from api.pages.router import router_pages
from api.weigh_ins.router import weigh_router

app = FastAPI()

app.mount("/static", StaticFiles(directory=API_PATH / "static"), name="static")

app.include_router(auth_router)
# app.include_router(
#     register_router,
#     prefix="/auth",
#     tags=["auth"],
# )
app.include_router(weigh_router)
app.include_router(router_pages)

# Keep it for debugging
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
