from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from src.core.database import get_db
from src.core.security import verify_token
from src.schemas import (
    TriviaQuestion, TriviaQuestionCreate, TriviaQuestionUpdate,
    LearningSession, LearningSessionCreate, LearningSessionUpdate,
    QuizSession, QuizAnswer
)
from src.services.learning_service import LearningService

router = APIRouter()


def get_current_user_id(token: str = Depends(verify_token)) -> int:
    """Extract user ID from JWT token."""
    return 1  # Placeholder


@router.get("/questions", response_model=List[TriviaQuestion])
async def get_trivia_questions(
    category: Optional[str] = None,
    difficulty_level: Optional[int] = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get trivia questions for learning."""
    learning_service = LearningService(db)
    questions = learning_service.get_trivia_questions(
        category=category,
        difficulty_level=difficulty_level,
        limit=limit
    )
    return questions


@router.post("/questions", response_model=TriviaQuestion)
async def create_trivia_question(
    question_data: TriviaQuestionCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Create a new trivia question (admin only)."""
    learning_service = LearningService(db)
    question = learning_service.create_trivia_question(question_data)
    return question


@router.get("/questions/{question_id}", response_model=TriviaQuestion)
async def get_trivia_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific trivia question."""
    learning_service = LearningService(db)
    question = learning_service.get_trivia_question(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trivia question not found"
        )
    return question


@router.put("/questions/{question_id}", response_model=TriviaQuestion)
async def update_trivia_question(
    question_id: int,
    question_update: TriviaQuestionUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Update a trivia question (admin only)."""
    learning_service = LearningService(db)
    
    question = learning_service.get_trivia_question(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trivia question not found"
        )
    
    updated_question = learning_service.update_trivia_question(question_id, question_update)
    return updated_question


@router.delete("/questions/{question_id}")
async def delete_trivia_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Delete a trivia question (admin only)."""
    learning_service = LearningService(db)
    
    question = learning_service.get_trivia_question(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trivia question not found"
        )
    
    learning_service.delete_trivia_question(question_id)
    return {"message": "Trivia question deleted successfully"}


@router.post("/quiz/start", response_model=QuizSession)
async def start_quiz_session(
    category: Optional[str] = None,
    difficulty_level: Optional[int] = None,
    num_questions: int = 10,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Start a new quiz session."""
    learning_service = LearningService(db)
    
    # Create learning session
    session_data = LearningSessionCreate(
        session_type="quiz",
        session_data={
            "category": category,
            "difficulty_level": difficulty_level,
            "num_questions": num_questions
        }
    )
    
    session = learning_service.create_learning_session(current_user_id, session_data)
    
    # Get questions for the quiz
    questions = learning_service.get_trivia_questions(
        category=category,
        difficulty_level=difficulty_level,
        limit=num_questions
    )
    
    return QuizSession(
        session_id=session.id,
        questions=questions,
        answers=[],
        total_score=0.0
    )


@router.post("/quiz/{session_id}/answer")
async def submit_quiz_answer(
    session_id: int,
    answer: QuizAnswer,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Submit an answer for a quiz question."""
    learning_service = LearningService(db)
    
    # Verify session belongs to user
    session = learning_service.get_learning_session(session_id, current_user_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning session not found"
        )
    
    # Get the question to verify answer
    question = learning_service.get_trivia_question(answer.question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Check if answer is correct
    is_correct = answer.user_answer.lower().strip() == question.correct_answer.lower().strip()
    
    # Update answer with correctness
    answer.is_correct = is_correct
    
    # Update learning session
    learning_service.update_learning_session_progress(
        session_id,
        questions_answered=1,
        correct_answers=1 if is_correct else 0
    )
    
    return {
        "is_correct": is_correct,
        "correct_answer": question.correct_answer,
        "explanation": question.explanation
    }


@router.post("/quiz/{session_id}/complete", response_model=LearningSession)
async def complete_quiz_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Complete a quiz session and calculate final score."""
    learning_service = LearningService(db)
    
    # Verify session belongs to user
    session = learning_service.get_learning_session(session_id, current_user_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning session not found"
        )
    
    # Calculate final score
    if session.questions_answered > 0:
        accuracy = session.correct_answers / session.questions_answered
        final_score = accuracy * 100
    else:
        final_score = 0.0
    
    # Update session with final score
    session_update = LearningSessionUpdate(
        total_score=final_score,
        completed_at=datetime.utcnow()
    )
    
    completed_session = learning_service.update_learning_session(session_id, session_update)
    return completed_session


@router.get("/sessions", response_model=List[LearningSession])
async def get_learning_sessions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Get user's learning sessions."""
    learning_service = LearningService(db)
    sessions = learning_service.get_user_learning_sessions(
        current_user_id, skip=skip, limit=limit
    )
    return sessions


@router.get("/sessions/{session_id}", response_model=LearningSession)
async def get_learning_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Get a specific learning session."""
    learning_service = LearningService(db)
    session = learning_service.get_learning_session(session_id, current_user_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning session not found"
        )
    return session


@router.get("/progress")
async def get_learning_progress(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Get user's learning progress and statistics."""
    learning_service = LearningService(db)
    progress = learning_service.get_user_progress(current_user_id)
    return progress

