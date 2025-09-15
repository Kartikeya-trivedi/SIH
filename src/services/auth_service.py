from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from datetime import datetime

from src.db.models.models import User, KolamImage, GeneratedKolam, TriviaQuestion, LearningSession
from src.schemas import (
    UserCreate, UserUpdate, KolamImageCreate, KolamImageUpdate, 
    GeneratedKolamCreate, GeneratedKolamUpdate, KolamImageAnalysis,
    TriviaQuestionCreate, TriviaQuestionUpdate, LearningSessionCreate, LearningSessionUpdate
)
from src.core.security import get_password_hash
from src.core.logging import LoggerMixin


class UserService(LoggerMixin):
    """Service for user-related operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        self.logger.info("User created", user_id=db_user.id, username=db_user.username)
        return db_user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get list of users."""
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user information."""
        db_user = self.get_user(user_id)
        if not db_user:
            return None
        
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db_user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_user)
        
        self.logger.info("User updated", user_id=user_id)
        return db_user
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user."""
        db_user = self.get_user(user_id)
        if not db_user:
            return False
        
        self.db.delete(db_user)
        self.db.commit()
        
        self.logger.info("User deleted", user_id=user_id)
        return True


class AuthService(LoggerMixin):
    """Service for authentication-related operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        return self.user_service.create_user(user_data)
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password."""
        user = self.user_service.get_user_by_username(username)
        if not user:
            return None
        
        from src.core.security import verify_password
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.user_service.get_user_by_username(username)
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user information."""
        return self.user_service.update_user(user_id, user_update)

