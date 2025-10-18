# app/models/user_model.py
import enum
from datetime import datetime
from sqlalchemy import Integer, Column, Float, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

import db


class PayoutStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class Payout(Base):
    __tablename__ = "payouts"

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime, nullable=False)
    currency = Column(String, nullable=False)
    status = Column(enum.Enum(PayoutStatus), nullable=False)
    user_id = Column(Integer, foreign_key="user.id", nullable=False)
    # description = Column(String(255), nullable=False)
    owner=relationship("User", back_populates="payouts")



