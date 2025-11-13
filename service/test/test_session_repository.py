"""
Unit tests for session repository.
"""
import pytest
from datetime import datetime, timedelta
from app.repositories.session_repository import SessionRepository
from app.repositories.user_repository import UserRepository
from app.models import Session


def test_create_session(test_db):
    """
    Test session creation.
    """
    # Create a user first
    user_repo = UserRepository(test_db)
    user = user_repo.create_user("test_user", "hashed_password")
    
    # Create session
    session_repo = SessionRepository(test_db)
    start_time = datetime.utcnow()
    max_time = start_time + timedelta(hours=1)
    session = session_repo.create_session(
        user_id=user.id,
        token="test_token",
        start_time=start_time,
        max_time=max_time
    )
    
    assert session.id is not None
    assert session.user_id == user.id
    assert session.token == "test_token"


def test_get_valid_session_by_user_id(test_db):
    """
    Test getting valid session by user_id.
    """
    # Create a user first
    user_repo = UserRepository(test_db)
    user = user_repo.create_user("test_user", "hashed_password")
    
    # Create session
    session_repo = SessionRepository(test_db)
    start_time = datetime.utcnow()
    max_time = start_time + timedelta(hours=1)
    session_repo.create_session(
        user_id=user.id,
        token="test_token",
        start_time=start_time,
        max_time=max_time
    )
    
    # Get valid session
    current_time = datetime.utcnow()
    session = session_repo.get_valid_session_by_user_id(user.id, current_time)
    assert session is not None
    assert session.token == "test_token"


def test_get_valid_session_expired(test_db):
    """
    Test getting expired session.
    """
    # Create a user first
    user_repo = UserRepository(test_db)
    user = user_repo.create_user("test_user", "hashed_password")
    
    # Create expired session
    session_repo = SessionRepository(test_db)
    start_time = datetime.utcnow() - timedelta(hours=2)
    max_time = start_time + timedelta(hours=1)  # Expired 1 hour ago
    session_repo.create_session(
        user_id=user.id,
        token="test_token",
        start_time=start_time,
        max_time=max_time
    )
    
    # Try to get valid session
    current_time = datetime.utcnow()
    session = session_repo.get_valid_session_by_user_id(user.id, current_time)
    assert session is None


def test_get_session_by_token(test_db):
    """
    Test getting session by token.
    """
    # Create a user first
    user_repo = UserRepository(test_db)
    user = user_repo.create_user("test_user", "hashed_password")
    
    # Create session
    session_repo = SessionRepository(test_db)
    start_time = datetime.utcnow()
    max_time = start_time + timedelta(hours=1)
    session_repo.create_session(
        user_id=user.id,
        token="test_token",
        start_time=start_time,
        max_time=max_time
    )
    
    # Get session by token
    session = session_repo.get_session_by_token("test_token")
    assert session is not None
    assert session.user_id == user.id


def test_is_session_valid(test_db):
    """
    Test session validity check.
    """
    # Create a user first
    user_repo = UserRepository(test_db)
    user = user_repo.create_user("test_user", "hashed_password")
    
    # Create session
    session_repo = SessionRepository(test_db)
    start_time = datetime.utcnow()
    max_time = start_time + timedelta(hours=1)
    session_repo.create_session(
        user_id=user.id,
        token="test_token",
        start_time=start_time,
        max_time=max_time
    )
    
    # Check validity
    current_time = datetime.utcnow()
    assert session_repo.is_session_valid("test_token", current_time) is True
    assert session_repo.is_session_valid("invalid_token", current_time) is False

