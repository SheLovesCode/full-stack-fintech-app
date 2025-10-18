# app/models/user_model.py
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    oauth_provider = Column(String, nullable=False)  # e.g., "google" or "github"
    oauth_id = Column(String, nullable=False, unique=True, index=True)  # ID from provider
    email = Column(String, nullable=True, unique=True, index=True)
    full_name = Column(String, nullable=True)
    profile_pic_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

Index('ix_oauth_id', User.oauth_id, unique=True)
