"""
Pydantic models for request and response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserSignUpRequest(BaseModel):
    """
    Request model for user sign up.
    
    Attributes:
        user_id: User identifier.
        password: User password.
    """
    user_id: str = Field(..., min_length=1, description="User identifier")
    password: str = Field(..., min_length=1, description="User password")


class UserSignUpResponse(BaseModel):
    """
    Response model for user sign up.
    
    Attributes:
        user_id: User identifier.
        message: Success message.
    """
    user_id: str
    message: str


class UserSignInRequest(BaseModel):
    """
    Request model for user sign in.
    
    Attributes:
        user_id: User identifier.
        password: User password.
    """
    user_id: str = Field(..., min_length=1, description="User identifier")
    password: str = Field(..., min_length=1, description="User password")


class SessionResponse(BaseModel):
    """
    Response model for session information.
    
    Attributes:
        token: Session token.
        user_id: User identifier.
        start_time: Session start timestamp.
        max_time: Session expiration timestamp.
    """
    token: str
    user_id: str
    start_time: datetime
    max_time: datetime
    
    class Config:
        from_attributes = True

