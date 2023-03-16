from pydantic import BaseModel, validator
from datetime import datetime, timedelta, timezone
from typing import Union, Optional, List
from schemas.user import User
from schemas.tag import Tag

JST = timezone(timedelta(hours=+9), "JST")


class ScheduleBase(BaseModel):
    user_id: int
    period_start: Optional[datetime]
    period_end: Optional[datetime]
    title: Union[str, None] = None
    memo: Union[str, None] = None


class ScheduleCreate(ScheduleBase):
    tag: List[int] = []
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.datetime.now(JST)


class ScheduleCreateResponse(ScheduleBase):
    id: int
    tag: List[Tag] = []
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class ScheduleDisplay(BaseModel):
    user: User
    period_start: Optional[datetime]
    period_end: Optional[datetime]
    title: Union[str, None] = None
    memo: Union[str, None] = None

    class Config:
        orm_mode = True


class Schedule(ScheduleBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class UserSchedule(ScheduleCreate):
    user_id: int
    name: str
    email: str
    schedules: List[Schedule] = []

    class Config:
        orm_mode = True
