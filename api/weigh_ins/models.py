from datetime import datetime

from sqlalchemy import TIMESTAMP, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from api.db.base_class import Base


class Weigh(Base):
    __tablename__ = "weigh-history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    datetime: Mapped[TIMESTAMP] = mapped_column(DateTime, default=datetime.utcnow)
    weigh: Mapped[int | float] = mapped_column(Float, nullable=False)
    notes: Mapped[str] = mapped_column(String)
