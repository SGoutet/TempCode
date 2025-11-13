"""
Database models for users and sessions.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    """
    User model representing a bank user.
    
    Attributes:
        id: Primary key.
        user_id: Unique user identifier.
        password_hash: Hashed password using Argon2.
        created_at: User creation timestamp.
        sessions: Relationship to user sessions.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")


class Session(Base):
    """
    Session model representing user authentication sessions.
    
    Attributes:
        id: Primary key.
        user_id: Foreign key to users table.
        token: Session token.
        start_time: Session start timestamp.
        max_time: Session expiration timestamp.
        user: Relationship to user.
    """
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    max_time = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="sessions")

