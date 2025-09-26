from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin
from app.utils.hash import hash_password, verify_password
from app.utils.jwt_handler import create_access_token

def register_user(db: Session, user: UserCreate):
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == user.email) | (User.username == user.username)
        ).first()
        
        if existing_user:
            if existing_user.email == user.email:
                raise ValueError("Email already registered")
            if existing_user.username == user.username:
                raise ValueError("Username already taken")
        
        # Create new user
        db_user = User(
            username=user.username, 
            email=user.email, 
            hashed_password=hash_password(user.password)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise ValueError("User already exists")

def login_user(db: Session, user: UserLogin):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        return None
    token = create_access_token({"sub": db_user.email})
    return token