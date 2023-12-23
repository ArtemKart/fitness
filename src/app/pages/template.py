from fastapi.templating import Jinja2Templates

from app.core.config import APP_PATH

templates = Jinja2Templates(directory=APP_PATH / "templates")
