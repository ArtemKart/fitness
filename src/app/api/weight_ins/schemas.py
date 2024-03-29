import datetime
from typing import Optional

from pydantic import BaseModel


class WeightCreate(BaseModel):
    weight: int | float
    notes: Optional[str]


class WeightRead(BaseModel):
    values: list[int | float]
    datetime: list[datetime.date]
