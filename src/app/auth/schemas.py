from pydantic import BaseModel


class UserRead(BaseModel):
    email: str
    name: str


class UserCreate(BaseModel):
    username: str
    email: str
    name: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Msg(BaseModel):
    msg: str
