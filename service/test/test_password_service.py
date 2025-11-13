"""
Unit tests for password service.
"""
import pytest
from app.services.password_service import PasswordService


def test_hash_password():
    """
    Test password hashing.
    """
    service = PasswordService()
    password = "test_password"
    hashed = service.hash_password(password)
    
    assert hashed is not None
    assert hashed != password
    assert len(hashed) > 0


def test_verify_password_correct():
    """
    Test password verification with correct password.
    """
    service = PasswordService()
    password = "test_password"
    hashed = service.hash_password(password)
    
    assert service.verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """
    Test password verification with incorrect password.
    """
    service = PasswordService()
    password = "test_password"
    wrong_password = "wrong_password"
    hashed = service.hash_password(password)
    
    assert service.verify_password(wrong_password, hashed) is False


def test_verify_password_different_hashes():
    """
    Test that same password produces different hashes.
    """
    service = PasswordService()
    password = "test_password"
    hashed1 = service.hash_password(password)
    hashed2 = service.hash_password(password)
    
    # Argon2 produces different hashes each time (due to salt)
    assert hashed1 != hashed2
    # But both verify correctly
    assert service.verify_password(password, hashed1) is True
    assert service.verify_password(password, hashed2) is True

