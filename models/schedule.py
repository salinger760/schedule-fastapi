from sqlalchemy import Column, Integer, String
from sqlalchemy.types import TIMESTAMP, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from datetime import datetime, timedelta, timezone
from database import Base
import models.tagging as model_tagging

JST = timezone(timedelta(hours=+9), "JST")


class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), default=0)
    period_start = Column(type_=TIMESTAMP(timezone=True))
    period_end = Column(type_=TIMESTAMP(timezone=True))
    title = Column(String(255), default="")
    memo = Column(String(255), default="")
    created_at = Column(
        type_=TIMESTAMP(timezone=True), nullable=False, default=datetime.now(JST)
    )
    updated_at = Column(
        type_=TIMESTAMP(timezone=True), nullable=False, default=datetime.now(JST)
    )
    version = Column(BigInteger, nullable=False)

    __mapper_args__ = {"version_id_col": version}

    user = relationship("User")
    tag = relationship(
        "Tag",
        secondary=model_tagging.Tagging.__tablename__,
        back_populates="schedule",
        lazy="joined",
    )
