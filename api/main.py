import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.auth.router import auth_router, register_router
from api.config import API_PATH
from api.pages.main_page.router import router_main
from api.pages.profile.router import router_profile
from api.weigh_ins.router import weigh_router

app = FastAPI()


app.mount("/static", StaticFiles(directory=API_PATH / "static"), name="static")

app.include_router(auth_router)
app.include_router(register_router)
app.include_router(router_main)
app.include_router(router_profile)
app.include_router(weigh_router)


# Keep it for debugging
if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
