"""
Integration tests for authentication routes.
"""
import pytest
from app.services.password_service import PasswordService


def test_signup_success(client):
    """
    Test successful user signup.
    """
    response = client.post(
        "/auth/signup",
        json={
            "user_id": "test_user",
            "password": "test_password"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == "test_user"
    assert "message" in data


def test_signup_duplicate_user(client):
    """
    Test signup with duplicate user_id.
    """
    # First signup
    client.post(
        "/auth/signup",
        json={
            "user_id": "test_user",
            "password": "test_password"
        }
    )
    
    # Second signup with same user_id
    response = client.post(
        "/auth/signup",
        json={
            "user_id": "test_user",
            "password": "test_password"
        }
    )
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_signin_success(client):
    """
    Test successful user signin.
    """
    # First signup
    client.post(
        "/auth/signup",
        json={
            "user_id": "test_user",
            "password": "test_password"
        }
    )
    
    # Then signin
    response = client.post(
        "/auth/signin",
        json={
            "user_id": "test_user",
            "password": "test_password"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["user_id"] == "test_user"
    assert "start_time" in data
    assert "max_time" in data


def test_signin_wrong_password(client):
    """
    Test signin with wrong password.
    """
    # First signup
    client.post(
        "/auth/signup",
        json={
            "user_id": "test_user",
            "password": "test_password"
        }
    )
    
    # Then signin with wrong password
    response = client.post(
        "/auth/signin",
        json={
            "user_id": "test_user",
            "password": "wrong_password"
        }
    )
    
    assert response.status_code == 401
    assert "Invalid" in response.json()["detail"]


def test_signin_nonexistent_user(client):
    """
    Test signin with non-existent user.
    """
    response = client.post(
        "/auth/signin",
        json={
            "user_id": "nonexistent_user",
            "password": "test_password"
        }
    )
    
    assert response.status_code == 401
    assert "Invalid" in response.json()["detail"]


def test_signin_existing_session(client):
    """
    Test that signin returns existing session if valid.
    """
    # First signup
    client.post(
        "/auth/signup",
        json={
            "user_id": "test_user",
            "password": "test_password"
        }
    )
    
    # First signin
    response1 = client.post(
        "/auth/signin",
        json={
            "user_id": "test_user",
            "password": "test_password"
        }
    )
    
    token1 = response1.json()["token"]
    
    # Second signin (should return same token)
    response2 = client.post(
        "/auth/signin",
        json={
            "user_id": "test_user",
            "password": "test_password"
        }
    )
    
    token2 = response2.json()["token"]
    assert token1 == token2

