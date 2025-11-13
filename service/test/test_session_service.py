"""
Unit tests for session service.
"""
import pytest
from datetime import datetime, timedelta
from app.services.session_service import SessionService
from app.repositories.user_repository import UserRepository


def test_create_session(test_db):
    """
    Test session creation.
    """
    # Create a user first
    user_repo = UserRepository(test_db)
    user = user_repo.create_user("test_user", "hashed_password")
    
    # Create session
    session_service = SessionService(test_db)
    token = session_service.create_session(user.id)
    
    assert token is not None
    assert len(token) > 0


def test_create_session_existing_valid(test_db):
    """
    Test that existing valid session is returned.
    """
    # Create a user first
    user_repo = UserRepository(test_db)
    user = user_repo.create_user("test_user", "hashed_password")
    
    # Create session
    session_service = SessionService(test_db)
    token1 = session_service.create_session(user.id)
    
    # Create another session (should return existing)
    token2 = session_service.create_session(user.id)
    
    assert token1 == token2


def test_get_session_info(test_db):
    """
    Test getting session information.
    """
    # Create a user first
    user_repo = UserRepository(test_db)
    user = user_repo.create_user("test_user", "hashed_password")
    
    # Create session
    session_service = SessionService(test_db)
    token = session_service.create_session(user.id)
    
    # Get session info
    session_info = session_service.get_session_info(token)
    assert session_info is not None
    assert session_info["token"] == token
    assert session_info["user_id"] == "test_user"
    assert "start_time" in session_info
    assert "max_time" in session_info


def test_get_session_info_invalid_token(test_db):
    """
    Test getting session info with invalid token.
    """
    session_service = SessionService(test_db)
    session_info = session_service.get_session_info("invalid_token")
    assert session_info is None

