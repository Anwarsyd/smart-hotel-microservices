# app/controllers/auth_controller.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, BackgroundTasks
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.schemas.token_schema import Token
from app.services.auth_service import (
    register_user,
    login_user,
    verify_user_email,
    resend_verification_email
)
from app.models.user import User


class AuthController:
    
    @staticmethod
    def register_new_user(
        user: UserCreate,
        db: Session,
        background_tasks: BackgroundTasks
    ) -> dict:
        """
        Register new user and send verification email
        
        Returns success message instead of user data
        """
        try:
            db_user = register_user(db, user, background_tasks)
            return {
                "message": "User registered successfully! Please check your email to verify your account.",
                "email": db_user.email,
                "username": db_user.username,
                "role": db_user.role
            }
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
    def verify_email(token: str, db: Session, background_tasks: BackgroundTasks) -> dict:
        """
        Verify user email with token
        """
        try:
            return verify_user_email(db, token, background_tasks)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred during email verification"
            )
    
    @staticmethod
    def resend_verification(email: str, db: Session, background_tasks: BackgroundTasks) -> dict:
        """
        Resend verification email to user
        """
        try:
            return resend_verification_email(db, email, background_tasks)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while resending verification email"
            )
    
    @staticmethod
    def authenticate_user(user: UserLogin, db: Session) -> Token:
        """
        Authenticate user and return JWT token
        
        Raises HTTPException if email not verified
        """
        try:
            token = login_user(db, user)
            
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            
            return Token(access_token=token, token_type="bearer")
            
        except ValueError as e:
            # Handle unverified email error
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred during authentication"
            )
    
    @staticmethod
    def get_user_profile(current_user: User) -> UserResponse:
        """
        Get current user profile
        """
        return UserResponse(
            id=current_user.id,
            username=current_user.username,
            email=current_user.email,
            role=current_user.role  # FIX: Include role field
        )