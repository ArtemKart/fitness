from typing import Optional

from pydantic import BaseModel
import datetime


class WeightCreate(BaseModel):
    weight: int | float
    notes: Optional[str]


class Msg(BaseModel):
    msg: str


class WeightRead(BaseModel):
    values: list[int | float]
    datetime: list[datetime.date]
