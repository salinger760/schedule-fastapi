from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime, timedelta, timezone


class UserBase(BaseModel):
    name: Optional[str] = "ああああ"
    email: Optional[str] = "test@example.com"
    is_active: bool


class UserEmail(BaseModel):
    email: str

class UserCreate(UserBase):
    hashed_password: str

class UserUpdate(UserBase):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.datetime.now(JST)

class UserCreateResponse(UserBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
