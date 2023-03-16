from pydantic import BaseModel


class TaggingBase(BaseModel):
    shedule_id: int
    tag_id: int


class TaggingCreate(TaggingBase):
    pass


class TaggingCreateResponse(TaggingCreate):
    id: int

    class Config:
        orm_mode = True


class Tagging(TaggingBase):
    id: int

    class Config:
        orm_mode = True
