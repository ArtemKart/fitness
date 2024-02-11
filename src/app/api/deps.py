from typing import Annotated

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.auth.actions.auth import get_current_user_from_token
from src.app.api.auth.base_config import oauth2_scheme
from src.app.db.models import User
from src.app.db.session import get_async_session


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]
CurrentUser = Annotated[User, Depends(get_current_user_from_token)]
