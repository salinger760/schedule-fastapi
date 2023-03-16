from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.types import TIMESTAMP, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone
from database import Base


JST = timezone(timedelta(hours=+9), "JST")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

    created_at = Column(
        type_=TIMESTAMP(timezone=True), nullable=False, default=datetime.now(JST)
    )
    updated_at = Column(
        type_=TIMESTAMP(timezone=True), nullable=False, default=datetime.now(JST)
    )
    version = Column(BigInteger, nullable=False)

    __mapper_args__ = {"version_id_col": version}

    # schedule = relationship("Schedule")

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "is_active": self.is_active,
        }
