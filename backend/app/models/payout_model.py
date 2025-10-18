# app/models/user_model.py
import enum
from datetime import datetime
from sqlalchemy import Integer, Column, Float, String, DateTime, Enum as SqlAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class PayoutStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class Payout(Base):
    __tablename__ = "payouts"

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)
    currency = Column(String, nullable=False)
    status = Column(SqlAlchemyEnum(PayoutStatus, native_enum=False), nullable=False, default=PayoutStatus.PENDING)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="payouts")