from fastapi.templating import Jinja2Templates

from api.config import API_PATH

templates = Jinja2Templates(directory=API_PATH / "templates")
