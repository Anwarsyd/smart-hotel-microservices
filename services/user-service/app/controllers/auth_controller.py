# app/controllers/auth_controller.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.schemas.token_schema import Token
from app.services.auth_service import register_user, login_user
from app.models.user import User


class AuthController:
    """
    Controller layer to handle authentication logic
    Separates route handling from business logic
    """
    
    @staticmethod
    def register_new_user(user: UserCreate, db: Session) -> UserResponse:
        """
        Handle user registration
        
        Args:
            user: UserCreate schema with registration data
            db: Database session
            
        Returns:
            UserResponse: Registered user data
            
        Raises:
            HTTPException: If registration fails
        """
        try:
            db_user = register_user(db, user)
            return UserResponse(
                id=db_user.id,
                username=db_user.username,
                email=db_user.email
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred during registration"
            )
    
    @staticmethod
    def authenticate_user(user: UserLogin, db: Session) -> Token:
        """
        Handle user login and return JWT token
        
        Args:
            user: UserLogin schema with credentials
            db: Database session
            
        Returns:
            Token: JWT access token
            
        Raises:
            HTTPException: If authentication fails
        """
        token = login_user(db, user)
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        return Token(access_token=token, token_type="bearer")
    
    @staticmethod
    def get_user_profile(current_user: User) -> UserResponse:
        """
        Get current authenticated user's profile
        
        Args:
            current_user: Authenticated user object
            
        Returns:
            UserResponse: User profile data
        """
        return UserResponse(
            id=current_user.id,
            username=current_user.username,
            email=current_user.email
        )