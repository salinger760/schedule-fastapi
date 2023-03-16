from pydantic import BaseModel, validator
from datetime import datetime, timedelta, timezone
from typing import Optional

JST = timezone(timedelta(hours=+9), "JST")


class TagBase(BaseModel):
    name: str = ""
    color: str = ""


class TagCreate(TagBase):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.datetime.now(JST)


class TagCreateResponse(TagBase):
    id: int

    class Config:
        orm_mode = True


class Tag(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
