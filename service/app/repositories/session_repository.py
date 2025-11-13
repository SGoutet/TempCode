"""
Repository for session database operations.
"""
from sqlalchemy.orm import Session as DBSession, joinedload
from sqlalchemy import select, and_
from typing import Optional
from datetime import datetime
from app.models import Session, User


class SessionRepository:
    """
    Repository for session-related database operations.
    """
    
    def __init__(self, db: DBSession):
        """
        Initialize repository with database session.
        
        Args:
            db: Database session instance.
        """
        self.db = db
    
    def create_session(
        self,
        user_id: int,
        token: str,
        start_time: datetime,
        max_time: datetime
    ) -> Session:
        """
        Create a new session in the database.
        
        Args:
            user_id: User ID (foreign key).
            token: Session token.
            start_time: Session start timestamp.
            max_time: Session expiration timestamp.
            
        Returns:
            Created session object.
        """
        session = Session(
            user_id=user_id,
            token=token,
            start_time=start_time,
            max_time=max_time
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def get_valid_session_by_user_id(self, user_id: int, current_time: datetime) -> Optional[Session]:
        """
        Get a valid session for a user that hasn't expired.
        
        Args:
            user_id: User ID.
            current_time: Current timestamp for validation.
            
        Returns:
            Valid session object if found, None otherwise.
        """
        stmt = select(Session).options(
            joinedload(Session.user)
        ).where(
            and_(
                Session.user_id == user_id,
                Session.max_time > current_time
            )
        ).order_by(Session.start_time.desc())
        result = self.db.scalars(stmt).first()
        return result
    
    def get_session_by_token(self, token: str) -> Optional[Session]:
        """
        Get a session by token.
        
        Args:
            token: Session token.
            
        Returns:
            Session object if found, None otherwise.
        """
        stmt = select(Session).options(
            joinedload(Session.user)
        ).where(Session.token == token)
        result = self.db.scalars(stmt).first()
        return result
    
    def is_session_valid(self, token: str, current_time: datetime) -> bool:
        """
        Check if a session is valid (exists and not expired).
        
        Args:
            token: Session token.
            current_time: Current timestamp for validation.
            
        Returns:
            True if session is valid, False otherwise.
        """
        session = self.get_session_by_token(token)
        if session is None:
            return False
        return session.max_time > current_time
    
    def delete_session(self, session: Session) -> None:
        """
        Delete a session from the database.
        
        Args:
            session: Session object to delete.
        """
        self.db.delete(session)
        self.db.commit()

