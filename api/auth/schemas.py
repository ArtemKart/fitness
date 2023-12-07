from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    email: str
    name: str


class UserCreate(schemas.BaseUserCreate):
    username: str
    name: str
