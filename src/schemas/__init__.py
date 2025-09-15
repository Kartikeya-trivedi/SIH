from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = None


class UserInDB(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class User(UserInDB):
    pass


# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


# Kolam Image Schemas
class KolamImageBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    is_public: bool = False


class KolamImageCreate(KolamImageBase):
    pass


class KolamImageUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    is_public: Optional[bool] = None


class KolamImageAnalysis(BaseModel):
    detected_patterns: List[str]
    confidence_scores: Dict[str, float]
    complexity_score: float
    symmetry_type: str
    geometric_features: Dict[str, Any]


class KolamImageInDB(KolamImageBase):
    id: int
    user_id: int
    filename: str
    file_path: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    detected_patterns: Optional[List[str]] = None
    confidence_scores: Optional[Dict[str, float]] = None
    complexity_score: Optional[float] = None
    symmetry_type: Optional[str] = None
    geometric_features: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class KolamImage(KolamImageInDB):
    pass


# Generated Kolam Schemas
class GeneratedKolamBase(BaseModel):
    pattern_type: str
    complexity_level: int = Field(..., ge=1, le=10)
    symmetry_type: Optional[str] = None
    size: str = Field(default="medium")
    title: Optional[str] = None
    description: Optional[str] = None


class GeneratedKolamCreate(GeneratedKolamBase):
    generation_params: Optional[Dict[str, Any]] = None


class GeneratedKolamUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_favorite: Optional[bool] = None


class GeneratedKolamInDB(GeneratedKolamBase):
    id: int
    user_id: int
    svg_data: Optional[str] = None
    image_path: Optional[str] = None
    generation_params: Optional[Dict[str, Any]] = None
    is_favorite: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class GeneratedKolam(GeneratedKolamInDB):
    pass


# Trivia Question Schemas
class TriviaQuestionBase(BaseModel):
    question_text: str
    question_type: str
    difficulty_level: int = Field(..., ge=1, le=5)
    options: Optional[List[str]] = None
    correct_answer: str
    explanation: Optional[str] = None
    image_path: Optional[str] = None
    audio_path: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None


class TriviaQuestionCreate(TriviaQuestionBase):
    pass


class TriviaQuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    image_path: Optional[str] = None
    audio_path: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class TriviaQuestionInDB(TriviaQuestionBase):
    id: int
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TriviaQuestion(TriviaQuestionInDB):
    pass


# Learning Session Schemas
class LearningSessionBase(BaseModel):
    session_type: str
    questions_answered: int = 0
    correct_answers: int = 0
    total_score: float = 0.0
    current_level: int = 1
    streak_days: int = 0
    session_data: Optional[Dict[str, Any]] = None


class LearningSessionCreate(LearningSessionBase):
    pass


class LearningSessionUpdate(BaseModel):
    questions_answered: Optional[int] = None
    correct_answers: Optional[int] = None
    total_score: Optional[float] = None
    current_level: Optional[int] = None
    streak_days: Optional[int] = None
    session_data: Optional[Dict[str, Any]] = None
    completed_at: Optional[datetime] = None


class LearningSessionInDB(LearningSessionBase):
    id: int
    user_id: int
    last_activity: datetime
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class LearningSession(LearningSessionInDB):
    pass


# Quiz Response Schemas
class QuizAnswer(BaseModel):
    question_id: int
    user_answer: str
    is_correct: bool
    time_taken: Optional[float] = None  # seconds


class QuizSession(BaseModel):
    session_id: int
    questions: List[TriviaQuestion]
    answers: List[QuizAnswer]
    total_score: float
    completed_at: Optional[datetime] = None

