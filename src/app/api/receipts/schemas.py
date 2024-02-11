from pydantic import BaseModel

class ReceiptCreate(BaseModel):
    name: str
    coocking_time: int
    food_items: dict[str, int | float]
    description: str


class ReceiptRead(BaseModel):
    name: str
    coocking_time: int
    food_items: dict[str, int | float]
    description: str
