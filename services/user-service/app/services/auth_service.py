# app/services/auth_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin
from app.utils.hash import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from app.utils.token_generator import generate_verification_token
from app.utils.email_service import send_verification_email, send_welcome_email
from fastapi import BackgroundTasks
import logging

logger = logging.getLogger(__name__)


def register_user(db: Session, user: UserCreate, background_tasks: BackgroundTasks) -> User:
    """
    Register a new user in the database and send verification email
    
    Args:
        db: Database session
        user: UserCreate schema with registration data
        background_tasks: FastAPI background tasks for async email sending
        
    Returns:
        User: Created user object
        
    Raises:
        ValueError: If user already exists or validation fails
    """
    try:
        # Check if email already exists
        existing_email = db.query(User).filter(User.email == user.email).first()
        if existing_email:
            logger.warning(f"Registration attempt with existing email: {user.email}")
            raise ValueError("Email already registered")
        
        # Check if username already exists
        existing_username = db.query(User).filter(User.username == user.username).first()
        if existing_username:
            logger.warning(f"Registration attempt with existing username: {user.username}")
            raise ValueError("Username already taken")
        
        # Generate verification token
        verification_token = generate_verification_token()
        verification_expires = datetime.utcnow() + timedelta(hours=24)
        
        # Create new user with hashed password
        hashed_pwd = hash_password(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_pwd,
            is_verified=False,
            verification_token=verification_token,
            verification_token_expires=verification_expires
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Send verification email in background
        background_tasks.add_task(
            send_verification_email,
            db_user.email,
            db_user.username,
            verification_token
        )
        
        logger.info(f"New user registered successfully: {db_user.email}")
        return db_user
        
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Database integrity error during registration: {str(e)}")
        raise ValueError("User registration failed due to database constraint")
    except ValueError:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise ValueError("An unexpected error occurred during registration")


def verify_user_email(db: Session, token: str, background_tasks: BackgroundTasks) -> dict:
    """
    Verify user email with token
    
    Args:
        db: Database session
        token: Verification token
        background_tasks: FastAPI background tasks for async email sending
        
    Returns:
        dict: Success message with user info
        
    Raises:
        ValueError: If token is invalid or expired
    """
    try:
        # Find user by verification token
        user = db.query(User).filter(User.verification_token == token).first()
        
        if not user:
            logger.warning(f"Verification attempt with invalid token: {token}")
            raise ValueError("Invalid verification token")
        
        if user.is_verified:
            logger.info(f"User already verified: {user.email}")
            raise ValueError("Email already verified")
        
        # Check if token is expired
        if user.verification_token_expires < datetime.utcnow():
            logger.warning(f"Expired verification token for user: {user.email}")
            raise ValueError("Verification token has expired. Please request a new one.")
        
        # Update user verification status
        user.is_verified = True
        user.verification_token = None
        user.verification_token_expires = None
        user.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(user)
        
        # Send welcome email in background
        background_tasks.add_task(
            send_welcome_email,
            user.email,
            user.username
        )
        
        logger.info(f"User verified successfully: {user.email}")
        return {
            "message": "Email verified successfully! You can now login.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }
        
    except ValueError:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error during email verification: {str(e)}")
        raise ValueError("An error occurred during email verification")


def resend_verification_email(db: Session, email: str, background_tasks: BackgroundTasks) -> dict:
    """
    Resend verification email to user
    
    Args:
        db: Database session
        email: User email address
        background_tasks: FastAPI background tasks
        
    Returns:
        dict: Success message
        
    Raises:
        ValueError: If user not found or already verified
    """
    try:
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            logger.warning(f"Resend verification attempt for non-existent email: {email}")
            raise ValueError("User not found")
        
        if user.is_verified:
            raise ValueError("Email already verified")
        
        # Generate new verification token
        verification_token = generate_verification_token()
        verification_expires = datetime.utcnow() + timedelta(hours=24)
        
        user.verification_token = verification_token
        user.verification_token_expires = verification_expires
        user.updated_at = datetime.utcnow()
        
        db.commit()
        
        # Send verification email in background
        background_tasks.add_task(
            send_verification_email,
            user.email,
            user.username,
            verification_token
        )
        
        logger.info(f"Verification email resent to: {email}")
        return {"message": "Verification email sent successfully. Please check your inbox."}
        
    except ValueError:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error resending verification email: {str(e)}")
        raise ValueError("An error occurred while resending verification email")


def login_user(db: Session, user: UserLogin) -> str | None:
    """
    Authenticate user and generate JWT token
    
    Args:
        db: Database session
        user: UserLogin schema with credentials
        
    Returns:
        str: JWT access token if authentication successful, None otherwise
        
    Raises:
        ValueError: If email not verified
    """
    try:
        # Find user by email
        db_user = db.query(User).filter(User.email == user.email).first()
        
        if not db_user:
            logger.warning(f"Login attempt with non-existent email: {user.email}")
            return None
        
        # Check if email is verified
        if not db_user.is_verified:
            logger.warning(f"Login attempt with unverified email: {user.email}")
            raise ValueError("Please verify your email before logging in")
        
        # Verify password
        if not verify_password(user.password, db_user.hashed_password):
            logger.warning(f"Failed login attempt for user: {user.email}")
            return None
        
        # Generate JWT token with user email as subject
        token_data = {
            "sub": db_user.email,
            "user_id": db_user.id,
            "username": db_user.username
        }
        token = create_access_token(token_data)
        
        logger.info(f"User logged in successfully: {db_user.email}")
        return token
        
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return None


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Retrieve user by email address
    
    Args:
        db: Database session
        email: User email address
        
    Returns:
        User object if found, None otherwise
    """
    try:
        return db.query(User).filter(User.email == email).first()
    except Exception as e:
        logger.error(f"Error fetching user by email: {str(e)}")
        return None


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    Retrieve user by ID
    
    Args:
        db: Database session
        user_id: User ID
        
    Returns:
        User object if found, None otherwise
    """
    try:
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        logger.error(f"Error fetching user by ID: {str(e)}")
        return None