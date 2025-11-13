"""
Unit tests for user repository.
"""
import pytest
from app.repositories.user_repository import UserRepository
from app.models import User


def test_create_user(test_db):
    """
    Test user creation.
    """
    repository = UserRepository(test_db)
    user = repository.create_user("test_user", "hashed_password")
    
    assert user.id is not None
    assert user.user_id == "test_user"
    assert user.password_hash == "hashed_password"


def test_get_user_by_user_id(test_db):
    """
    Test getting user by user_id.
    """
    repository = UserRepository(test_db)
    repository.create_user("test_user", "hashed_password")
    
    user = repository.get_user_by_user_id("test_user")
    assert user is not None
    assert user.user_id == "test_user"


def test_get_user_by_user_id_not_found(test_db):
    """
    Test getting non-existent user.
    """
    repository = UserRepository(test_db)
    user = repository.get_user_by_user_id("non_existent_user")
    assert user is None


def test_user_exists(test_db):
    """
    Test user existence check.
    """
    repository = UserRepository(test_db)
    repository.create_user("test_user", "hashed_password")
    
    assert repository.user_exists("test_user") is True
    assert repository.user_exists("non_existent_user") is False

