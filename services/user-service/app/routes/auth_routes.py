# app/routes/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.schemas.token_schema import Token
from app.controllers.auth_controller import AuthController
from app.utils.jwt_handler import verify_token
from app.utils.role_checker import require_admin, require_staff_or_admin
from app.models.user import User
from pydantic import EmailStr


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
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account and send verification email"
)
def register(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    **User Registration Endpoint**
    
    - **username**: Unique username (3-50 characters, alphanumeric + underscore)
    - **email**: Valid email address
    - **password**: Password (min 8 chars, must contain uppercase, lowercase, and digit)
    - **role**: User role (admin, staff, or customer) - defaults to customer
    
    Returns success message. User must verify email before logging in.
    """
    return AuthController.register_new_user(user, db, background_tasks)


@router.get(
    "/verify",
    summary="Verify email address",
    description="Verify user email with token from verification link"
)
def verify_email(
    token: str = Query(..., description="Verification token from email"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    """
    **Email Verification Endpoint**
    
    - **token**: Verification token from email link
    
    Verifies the user's email and sends welcome email.
    """
    return AuthController.verify_email(token, db, background_tasks)


@router.post(
    "/resend-verification",
    summary="Resend verification email",
    description="Request a new verification email"
)
def resend_verification(
    email: EmailStr,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    **Resend Verification Email**
    
    - **email**: Email address to resend verification to
    
    Generates new token and sends verification email.
    """
    return AuthController.resend_verification(email, db, background_tasks)


@router.post(
    "/login",
    response_model=Token,
    summary="User login",
    description="Authenticate user and return JWT access token"
)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    **User Login Endpoint**
    
    - **email**: Registered and verified email address
    - **password**: User password
    
    Returns a JWT access token valid for 30 minutes.
    
    **Note**: Email must be verified before login.
    """
    return AuthController.authenticate_user(user, db)


# ============= Protected Routes (Any Authenticated User) =============
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
    
    Returns current authenticated user's profile including role
    """
    return AuthController.get_user_profile(current_user)


# ============= Admin Only Routes =============
@router.get(
    "/admin/users",
    summary="Get all users (Admin only)",
    description="Retrieve list of all users - Admin access required"
)
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    **Get All Users - Admin Only**
    
    Requires: Admin role
    
    Returns list of all registered users
    """
    # Check admin role
    require_admin(current_user)
    
    users = db.query(User).all()
    return {
        "total_users": len(users),
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "is_verified": user.is_verified,
                "created_at": user.created_at
            }
            for user in users
        ]
    }


@router.delete(
    "/admin/users/{user_id}",
    summary="Delete user (Admin only)",
    description="Delete a user by ID - Admin access required"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    **Delete User - Admin Only**
    
    Requires: Admin role
    
    Deletes a user from the system
    """
    # Check admin role
    require_admin(current_user)
    
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    
    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from deleting themselves
    if user_to_delete.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    db.delete(user_to_delete)
    db.commit()
    
    return {"message": f"User {user_to_delete.username} deleted successfully"}


# ============= Staff or Admin Routes =============
@router.get(
    "/staff/dashboard",
    summary="Staff dashboard (Staff/Admin only)",
    description="Access staff dashboard - Staff or Admin access required"
)
def staff_dashboard(
    current_user: User = Depends(get_current_user)
):
    """
    **Staff Dashboard - Staff/Admin Only**
    
    Requires: Staff or Admin role
    
    Returns staff-specific information
    """
    # Check staff or admin role
    require_staff_or_admin(current_user)
    
    return {
        "message": "Welcome to Staff Dashboard",
        "user": {
            "username": current_user.username,
            "role": current_user.role,
            "email": current_user.email
        },
        "access_level": "staff" if current_user.role == "staff" else "admin"
    }


# ============= Example Protected Route =============
@router.get(
    "/protected",
    summary="Protected route example",
    description="Example of a protected route that requires authentication"
)
def protected_route(current_user: User = Depends(get_current_user)):
    """
    **Protected Route Example**
    
    This is a sample protected route accessible by any authenticated user.
    """
    return {
        "message": "Access granted to protected resource",
        "user_id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "is_verified": current_user.is_verified
    }