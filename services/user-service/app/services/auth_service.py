# app/services/auth_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin
from app.utils.hash import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
import logging

# Set up logging
logger = logging.getLogger(__name__)


def register_user(db: Session, user: UserCreate) -> User:
    """
    Register a new user in the database
    
    Args:
        db: Database session
        user: UserCreate schema with registration data
        
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
        
        # Create new user with hashed password
        hashed_pwd = hash_password(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_pwd
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"New user registered successfully: {db_user.email}")
        return db_user
        
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Database integrity error during registration: {str(e)}")
        raise ValueError("User registration failed due to database constraint")
    except ValueError:
        # Re-raise ValueError as-is
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise ValueError("An unexpected error occurred during registration")


def login_user(db: Session, user: UserLogin) -> str | None:
    """
    Authenticate user and generate JWT token
    
    Args:
        db: Database session
        user: UserLogin schema with credentials
        
    Returns:
        str: JWT access token if authentication successful, None otherwise
    """
    try:
        # Find user by email
        db_user = db.query(User).filter(User.email == user.email).first()
        
        if not db_user:
            logger.warning(f"Login attempt with non-existent email: {user.email}")
            return None
        
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