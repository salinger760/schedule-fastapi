from typing import Optional
from pydantic import BaseModel
import os

CSRF_KEY = os.environ.get("CSRF_KEY")


class CsrfSettings(BaseModel):
    secret_key: str = CSRF_KEY


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class Csrf(BaseModel):
    csrf_token: str


class VerifyLogin(BaseModel):
    verify_login: bool


class SuccessMsg(BaseModel):
    message: str


class UserBody(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class UserInfo(BaseModel):
    id: Optional[str] = None
    email: str
