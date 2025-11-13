"""
Repository for user database operations.
"""
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import select
from typing import Optional
from app.models import User


class UserRepository:
    """
    Repository for user-related database operations.
    """
    
    def __init__(self, db: DBSession):
        """
        Initialize repository with database session.
        
        Args:
            db: Database session instance.
        """
        self.db = db
    
    def create_user(self, user_id: str, password_hash: str) -> User:
        """
        Create a new user in the database.
        
        Args:
            user_id: User identifier.
            password_hash: Hashed password.
            
        Returns:
            Created user object.
        """
        user = User(user_id=user_id, password_hash=password_hash)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user_by_user_id(self, user_id: str) -> Optional[User]:
        """
        Get a user by user_id.
        
        Args:
            user_id: User identifier.
            
        Returns:
            User object if found, None otherwise.
        """
        stmt = select(User).where(User.user_id == user_id)
        result = self.db.scalars(stmt).first()
        return result
    
    def user_exists(self, user_id: str) -> bool:
        """
        Check if a user exists by user_id.
        
        Args:
            user_id: User identifier.
            
        Returns:
            True if user exists, False otherwise.
        """
        user = self.get_user_by_user_id(user_id)
        return user is not None

