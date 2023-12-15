from pydantic import BaseModel


class UserRead(BaseModel):
    email: str
    name: str


class UserCreate(BaseModel):
    username: str
    name: str


class Token(BaseModel):
    access_token: str
    token_type: str
