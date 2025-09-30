# app/utils/token_generator.py
import uuid
import secrets


def generate_verification_token() -> str:
    """
    Generate a secure random verification token
    
    Returns:
        str: Random UUID token
    """
    return str(uuid.uuid4())


def generate_secure_token(length: int = 32) -> str:
    """
    Generate a secure random token using secrets module
    
    Args:
        length: Token length (default 32 characters)
        
    Returns:
        str: Secure random token
    """
    return secrets.token_urlsafe(length)