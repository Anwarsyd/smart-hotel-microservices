# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from datetime import datetime
from app.database.database import Base
import enum

class UserRole(str, enum.Enum):
    """User role enumeration"""
    ADMIN = "admin"
    STAFF = "staff"
    CUSTOMER = "customer"

class User(Base):
    __tablename__ = "users"  
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Role field with default 'customer'
    role = Column(String, default=UserRole.CUSTOMER.value, nullable=False)
    
    # Email verification fields
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_token = Column(String, nullable=True, unique=True)
    verification_token_expires = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)