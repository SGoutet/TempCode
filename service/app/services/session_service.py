"""
Session management service.
"""
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session as DBSession
from secrets import token_urlsafe
from app.repositories.session_repository import SessionRepository
from app.config import settings


class SessionService:
    """
    Service for session management and token generation.
    """
    
    def __init__(self, db: DBSession):
        """
        Initialize session service with database session.
        
        Args:
            db: Database session instance.
        """
        self.db = db
        self.session_repository = SessionRepository(db)
    
    def create_session(self, user_id: int) -> str:
        """
        Create a new session for a user.
        If a valid session exists, return the existing token.
        Otherwise, create a new session.
        
        Args:
            user_id: User ID.
            
        Returns:
            Session token.
        """
        current_time = datetime.utcnow()
        
        # Check if valid session exists
        existing_session = self.session_repository.get_valid_session_by_user_id(
            user_id,
            current_time
        )
        
        if existing_session is not None:
            return existing_session.token
        
        # Create new session
        token = token_urlsafe(32)
        start_time = current_time
        max_time = start_time + timedelta(seconds=settings.session_max_age_seconds)
        
        self.session_repository.create_session(
            user_id=user_id,
            token=token,
            start_time=start_time,
            max_time=max_time
        )
        
        return token
    
    def get_session_info(self, token: str) -> Optional[dict]:
        """
        Get session information by token.
        
        Args:
            token: Session token.
            
        Returns:
            Dictionary with session info if valid, None otherwise.
        """
        current_time = datetime.utcnow()
        session = self.session_repository.get_session_by_token(token)
        
        if session is None:
            return None
        
        if session.max_time <= current_time:
            return None
        
        return {
            "token": session.token,
            "user_id": session.user.user_id,
            "start_time": session.start_time,
            "max_time": session.max_time
        }

