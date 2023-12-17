from sqlalchemy import Boolean, TIMESTAMP, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from api.db.base_class import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[int] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String, default="Anonymous")
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)


class Weigh(Base):
    __tablename__ = "weigh-history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    datetime: Mapped[TIMESTAMP] = mapped_column(DateTime, default=datetime.utcnow)
    weigh: Mapped[int | float] = mapped_column(Float, nullable=False)
    notes: Mapped[str] = mapped_column(String)
