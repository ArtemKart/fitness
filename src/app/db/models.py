from datetime import datetime

from sqlalchemy import (
    Boolean,
    TIMESTAMP,
    Integer,
    Float,
    PickleType,
    String,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.app.db.base_class import Base


class User(Base):
    """
    User class contains user data.

    Attributes
    ----------
    id (int): user id.
    username (str): username.
    email (str): email.
    name (str): user first name or full name. Defaults to "Anonymous".
    is_active (bool): user active status.
    hashed_password (str): password hashed by Hasher.

    """

    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String, default="Anonymous")
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)


class Weight(Base):
    """
    Weight class contains weight data related to the specific user

    Attributes
    ----------
    id (int): weight id.
    user_id (int): foreign key relationship with User table.
    datetime (TIMESTAMP): the time when record was created. Format: "YYYY-MM-DD HH:MM:SS".
    weight (int | float): weight's value.
    notes (str): additional information to add.
     """

    __tablename__ = "weight-history"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    datetime: Mapped[TIMESTAMP] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    weight: Mapped[int | float] = mapped_column(Float, nullable=False)
    notes: Mapped[str] = mapped_column(String)


class Receipt(Base):
    """
    Receipt class contain added receip data

    Attributes
    ----------
    id (int): receipt id.
    user_id (int): foreign key relationship with User table.
    name (str): receipt name.
    coocking_time (int): estimated coocking time.
    food_items (dict[str, int | float]): needed food items and their 
        amounts/portions.
    description (str): described coocking process in details.
     """

    __tablename__ = "receipt"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(String)
    coocking_time: Mapped[int] = mapped_column(Integer, default=None)
    food_items: Mapped[dict[str, int | float]] = mapped_column(PickleType)
    description: Mapped[str] = mapped_column(Text)
