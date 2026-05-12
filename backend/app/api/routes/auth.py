"""
Authentication API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    - **name**: Full name (required)
    - **email**: Email address (required, must be unique)
    - **password**: Password (required, minimum 8 characters)
    """
    user = AuthService.register_user(db, user_data)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login with email and password.
    
    Returns JWT access token and refresh token.
    """
    user = AuthService.authenticate_user(db, credentials.email, credentials.password)
    tokens = AuthService.generate_tokens(user)
    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    
    Note: In production, validate refresh token from request body.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Refresh endpoint not yet implemented"
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: dict = Depends(lambda token: token),
    db: Session = Depends(get_db)
):
    """Get current authenticated user."""
    user = AuthService.get_user_by_id(db, current_user["user_id"])
    return user
