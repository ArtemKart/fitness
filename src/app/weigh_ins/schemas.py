from pydantic import BaseModel


class WeighCreate(BaseModel):
    weigh: int | float
    notes: str
