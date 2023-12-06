from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from api.db.base_class import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[int] = mapped_column(String)
    name: Mapped[str] = mapped_column(String, default="Anonymous")
