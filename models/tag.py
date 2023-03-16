from sqlalchemy import Column, Integer, String
from sqlalchemy.types import TIMESTAMP, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone
from database import Base
import models.tagging as model_tagging

JST = timezone(timedelta(hours=+9), "JST")


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), default="")
    color = Column(String(255), default="")
    created_at = Column(
        type_=TIMESTAMP(timezone=True), nullable=False, default=datetime.now(JST)
    )
    updated_at = Column(
        type_=TIMESTAMP(timezone=True), nullable=False, default=datetime.now(JST)
    )
    version = Column(BigInteger, nullable=False)

    __mapper_args__ = {'version_id_col': version}
    
    schedule = relationship("Schedule", secondary=model_tagging.Tagging.__tablename__, back_populates='tag', lazy="joined")