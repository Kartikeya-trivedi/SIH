# src/schemas/__init__.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# -------------------------
# User Schemas
# -------------------------
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

# -------------------------
# Authentication Schemas
# -------------------------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

# -------------------------
# Trivia Question Schemas
# -------------------------
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

# -------------------------
# Learning Session Schemas
# -------------------------
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

# -------------------------
# Quiz Response Schemas
# -------------------------
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

# -------------------------
# Kolam Generation / Knowledge Schemas
# -------------------------
class KolamGenerationRequest(BaseModel):
    query: str = Field(..., description="User query for generating a Kolam image")

class KolamGenerationResponse(BaseModel):
    image_url: str = Field(..., description="URL or path of the generated Kolam image")

class KnowledgeRequest(BaseModel):
    query: str = Field(..., description="User query for knowledge retrieval")
    generate_image: bool = Field(default=True, description="Whether to generate an image")

class KnowledgeResponse(BaseModel):
    explanation: str = Field(..., description="Textual explanation of the query")
    image_base64: Optional[str] = Field(None, description="Base64-encoded generated image, if requested")

# -------------------------
# Kolam Prediction Schemas
# -------------------------
class PredictionResponse(BaseModel):
    """
    Response schema for Kolam image prediction.
    User uploads an image, and we return the top class only.
    """
    label: str = Field(..., description="Predicted Kolam class")
    confidence: float = Field(..., description="Confidence score in %")
    design_principle: str = Field(..., description="Associated design principle for the predicted class")
