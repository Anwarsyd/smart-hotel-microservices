# app/utils/role_checker.py
from fastapi import HTTPException, status
from app.models.user import User
from typing import List


def check_user_role(user: User, allowed_roles: List[str]) -> bool:
    """
    Check if user has one of the allowed roles
    
    Args:
        user: User object
        allowed_roles: List of allowed roles
        
    Returns:
        bool: True if user has allowed role, False otherwise
    """
    return user.role in allowed_roles


def require_admin(current_user: User):
    """
    Dependency to require admin role
    
    Args:
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If user is not admin
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )


def require_staff_or_admin(current_user: User):
    """
    Dependency to require staff or admin role
    
    Args:
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If user is not staff or admin
    """
    if current_user.role not in ["admin", "staff"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff or Admin access required"
        )


def require_customer(current_user: User):
    """
    Dependency to require customer role
    
    Args:
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If user is not customer
    """
    if current_user.role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer access required"
        )