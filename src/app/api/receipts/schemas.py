from pydantic import BaseModel


class ReceiptCreate(BaseModel):
    id: int
    user_id: int
    name: str
    coocking_time: int
    food_items: dict[str, int | float]
    description: str
