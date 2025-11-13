"""
Authentication routes for user sign up and sign in.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DBSession
from typing import Annotated

from app.database import get_db
from app.schemas import UserSignUpRequest, UserSignUpResponse, UserSignInRequest, SessionResponse
from app.repositories.user_repository import UserRepository
from app.services.password_service import PasswordService
from app.services.session_service import SessionService

router = APIRouter(prefix="/auth", tags=["authentication"])

password_service = PasswordService()


def get_user_repository(db: Annotated[DBSession, Depends(get_db)]) -> UserRepository:
    """
    Dependency to get user repository.
    
    Args:
        db: Database session.
        
    Returns:
        UserRepository instance.
    """
    return UserRepository(db)


def get_session_service(db: Annotated[DBSession, Depends(get_db)]) -> SessionService:
    """
    Dependency to get session service.
    
    Args:
        db: Database session.
        
    Returns:
        SessionService instance.
    """
    return SessionService(db)


@router.post(
    "/signup",
    response_model=UserSignUpResponse,
    status_code=status.HTTP_201_CREATED
)
async def signup(
    request: UserSignUpRequest,
    user_repository: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserSignUpResponse:
    """
    Sign up a new user.
    
    Args:
        request: Sign up request with user_id and password.
        user_repository: User repository instance.
        
    Returns:
        Sign up response with user_id and message.
        
    Raises:
        HTTPException: If user already exists.
    """
    if user_repository.user_exists(request.user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    
    password_hash = password_service.hash_password(request.password)
    user = user_repository.create_user(request.user_id, password_hash)
    
    return UserSignUpResponse(
        user_id=user.user_id,
        message="User created successfully"
    )


@router.post(
    "/signin",
    response_model=SessionResponse,
    status_code=status.HTTP_200_OK
)
async def signin(
    request: UserSignInRequest,
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    session_service: Annotated[SessionService, Depends(get_session_service)]
) -> SessionResponse:
    """
    Sign in a user and create a session.
    
    Args:
        request: Sign in request with user_id and password.
        user_repository: User repository instance.
        session_service: Session service instance.
        
    Returns:
        Session response with token and session information.
        
    Raises:
        HTTPException: If user not found or password is incorrect.
    """
    user = user_repository.get_user_by_user_id(request.user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user_id or password"
        )
    
    if not password_service.verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user_id or password"
        )
    
    token = session_service.create_session(user.id)
    session_info = session_service.get_session_info(token)
    
    if session_info is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create session"
        )
    
    return SessionResponse(**session_info)

