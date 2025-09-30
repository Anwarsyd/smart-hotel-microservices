# app/routes/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.schemas.token_schema import Token
from app.controllers.auth_controller import AuthController
from app.utils.jwt_handler import verify_token
from app.models.user import User


security = HTTPBearer()
router = APIRouter(prefix="/auth", tags=["Authentication"])


# ============= Dependency for Protected Routes =============
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user from JWT token
    
    Args:
        credentials: Bearer token from Authorization header
        db: Database session
        
    Returns:
        User: Authenticated user object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


# ============= Public Routes =============
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email, username, and password"
)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    **User Registration Endpoint**
    
    - **username**: Unique username (3-50 characters)
    - **email**: Valid email address
    - **password**: Password (min 8 characters)
    
    Returns the created user details (without password)
    """
    return AuthController.register_new_user(user, db)


@router.post(
    "/login",
    response_model=Token,
    summary="User login",
    description="Authenticate user and return JWT access token"
)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    **User Login Endpoint**
    
    - **email**: Registered email address
    - **password**: User password
    
    Returns a JWT access token valid for 30 minutes
    """
    return AuthController.authenticate_user(user, db)


# ============= Protected Routes =============
@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Retrieve authenticated user's profile information"
)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    **Get Current User Profile**
    
    Requires: Bearer token in Authorization header
    
    Returns current authenticated user's profile
    """
    return AuthController.get_user_profile(current_user)


@router.get(
    "/protected",
    summary="Protected route example",
    description="Example of a protected route that requires authentication"
)
def protected_route(current_user: User = Depends(get_current_user)):
    """
    **Protected Route Example**
    
    This is a sample protected route to demonstrate JWT authentication.
    Replace this with your actual business logic.
    """
    return {
        "message": "Access granted to protected resource",
        "user_id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }