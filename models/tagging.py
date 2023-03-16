from sqlalchemy import Column, Integer
from sqlalchemy.sql.schema import ForeignKey
from datetime import timedelta, timezone
from database import Base

JST = timezone(timedelta(hours=+9), "JST")


class Tagging(Base):
    __tablename__ = "tagging"

    schedule_id = Column(
        Integer,
        ForeignKey("schedule.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    tag_id = Column(
        Integer,
        ForeignKey("tag.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
