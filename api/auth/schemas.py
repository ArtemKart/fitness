from typing import Optional

from pydantic import BaseModel
from fastapi import Request


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

# class LoginForm(BaseModel):
#     request: Request
#     username: Optional[str] = None
#     password: Optional[str] = None
#
#     async def create_oauth_form(self):
#         form = await self.request.form()
#         self.username = form.get("email")
#         self.password = form.get("password")
#
