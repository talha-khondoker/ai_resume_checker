"""
Authentication service for user management.
"""
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.models import User, UserRole
from app.schemas.schemas import UserCreate, TokenResponse
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token
)


class AuthService:
    """Service for authentication operations."""
    
    @staticmethod
    def register_user(db: Session, user_create: UserCreate) -> User:
        """
        Register a new user.
        
        Args:
            db: Database session
            user_create: User creation data
        
        Returns:
            Created user
        
        Raises:
            HTTPException: If user already exists
        """
        # Check if user exists
        existing_user = db.query(User).filter(
            User.email == user_create.email
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        hashed_password = get_password_hash(user_create.password)
        user = User(
            name=user_create.name,
            email=user_create.email,
            password=hashed_password,
            role=UserRole.USER,
            is_active=True
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        """
        Authenticate user with email and password.
        
        Args:
            db: Database session
            email: User email
            password: User password
        
        Returns:
            Authenticated user
        
        Raises:
            HTTPException: If credentials are invalid
        """
        user = db.query(User).filter(User.email == email).first()
        
        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        return user
    
    @staticmethod
    def generate_tokens(user: User) -> TokenResponse:
        """
        Generate access and refresh tokens for user.
        
        Args:
            user: User object
        
        Returns:
            TokenResponse with tokens
        """
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=1800  # 30 minutes in seconds
        )
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Get user by ID."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
