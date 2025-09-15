from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import Optional, List, Dict, Any
from datetime import datetime

from src.db.models.models import TriviaQuestion, LearningSession
from src.schemas import (
    TriviaQuestionCreate, TriviaQuestionUpdate, LearningSessionCreate, LearningSessionUpdate
)
from src.core.logging import LoggerMixin


class LearningService(LoggerMixin):
    """Service for learning-related operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Trivia Question operations
    def create_trivia_question(self, question_data: TriviaQuestionCreate) -> TriviaQuestion:
        """Create a new trivia question."""
        db_question = TriviaQuestion(
            question_text=question_data.question_text,
            question_type=question_data.question_type,
            difficulty_level=question_data.difficulty_level,
            options=question_data.options,
            correct_answer=question_data.correct_answer,
            explanation=question_data.explanation,
            image_path=question_data.image_path,
            audio_path=question_data.audio_path,
            category=question_data.category,
            tags=question_data.tags
        )
        self.db.add(db_question)
        self.db.commit()
        self.db.refresh(db_question)
        
        self.logger.info("Trivia question created", question_id=db_question.id)
        return db_question
    
    def get_trivia_question(self, question_id: int) -> Optional[TriviaQuestion]:
        """Get trivia question by ID."""
        return self.db.query(TriviaQuestion).filter(
            and_(TriviaQuestion.id == question_id, TriviaQuestion.is_active == True)
        ).first()
    
    def get_trivia_questions(
        self,
        category: Optional[str] = None,
        difficulty_level: Optional[int] = None,
        limit: int = 10
    ) -> List[TriviaQuestion]:
        """Get trivia questions with optional filters."""
        query = self.db.query(TriviaQuestion).filter(TriviaQuestion.is_active == True)
        
        if category:
            query = query.filter(TriviaQuestion.category == category)
        
        if difficulty_level:
            query = query.filter(TriviaQuestion.difficulty_level == difficulty_level)
        
        return query.limit(limit).all()
    
    def update_trivia_question(
        self,
        question_id: int,
        question_update: TriviaQuestionUpdate
    ) -> Optional[TriviaQuestion]:
        """Update trivia question."""
        db_question = self.get_trivia_question(question_id)
        if not db_question:
            return None
        
        update_data = question_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_question, field, value)
        
        db_question.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_question)
        
        self.logger.info("Trivia question updated", question_id=question_id)
        return db_question
    
    def delete_trivia_question(self, question_id: int) -> bool:
        """Delete a trivia question (soft delete)."""
        db_question = self.get_trivia_question(question_id)
        if not db_question:
            return False
        
        db_question.is_active = False
        db_question.updated_at = datetime.utcnow()
        self.db.commit()
        
        self.logger.info("Trivia question deleted", question_id=question_id)
        return True
    
    # Learning Session operations
    def create_learning_session(
        self,
        user_id: int,
        session_data: LearningSessionCreate
    ) -> LearningSession:
        """Create a new learning session."""
        db_session = LearningSession(
            user_id=user_id,
            session_type=session_data.session_type,
            questions_answered=session_data.questions_answered,
            correct_answers=session_data.correct_answers,
            total_score=session_data.total_score,
            current_level=session_data.current_level,
            streak_days=session_data.streak_days,
            session_data=session_data.session_data
        )
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        
        self.logger.info("Learning session created", session_id=db_session.id, user_id=user_id)
        return db_session
    
    def get_learning_session(self, session_id: int, user_id: int) -> Optional[LearningSession]:
        """Get learning session by ID for a specific user."""
        return self.db.query(LearningSession).filter(
            and_(LearningSession.id == session_id, LearningSession.user_id == user_id)
        ).first()
    
    def get_user_learning_sessions(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[LearningSession]:
        """Get user's learning sessions."""
        return self.db.query(LearningSession).filter(
            LearningSession.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def update_learning_session(
        self,
        session_id: int,
        session_update: LearningSessionUpdate
    ) -> Optional[LearningSession]:
        """Update learning session."""
        db_session = self.db.query(LearningSession).filter(
            LearningSession.id == session_id
        ).first()
        if not db_session:
            return None
        
        update_data = session_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_session, field, value)
        
        self.db.commit()
        self.db.refresh(db_session)
        
        self.logger.info("Learning session updated", session_id=session_id)
        return db_session
    
    def update_learning_session_progress(
        self,
        session_id: int,
        questions_answered: int = 0,
        correct_answers: int = 0
    ) -> Optional[LearningSession]:
        """Update learning session progress."""
        db_session = self.db.query(LearningSession).filter(
            LearningSession.id == session_id
        ).first()
        if not db_session:
            return None
        
        db_session.questions_answered += questions_answered
        db_session.correct_answers += correct_answers
        db_session.last_activity = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_session)
        
        return db_session
    
    def get_user_progress(self, user_id: int) -> Dict[str, Any]:
        """Get user's learning progress and statistics."""
        # Get total sessions
        total_sessions = self.db.query(LearningSession).filter(
            LearningSession.user_id == user_id
        ).count()
        
        # Get completed sessions
        completed_sessions = self.db.query(LearningSession).filter(
            and_(
                LearningSession.user_id == user_id,
                LearningSession.completed_at.isnot(None)
            )
        ).count()
        
        # Get average score
        avg_score = self.db.query(func.avg(LearningSession.total_score)).filter(
            and_(
                LearningSession.user_id == user_id,
                LearningSession.completed_at.isnot(None)
            )
        ).scalar() or 0.0
        
        # Get total questions answered
        total_questions = self.db.query(func.sum(LearningSession.questions_answered)).filter(
            LearningSession.user_id == user_id
        ).scalar() or 0
        
        # Get total correct answers
        total_correct = self.db.query(func.sum(LearningSession.correct_answers)).filter(
            LearningSession.user_id == user_id
        ).scalar() or 0
        
        # Calculate accuracy
        accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0.0
        
        # Get current streak
        current_session = self.db.query(LearningSession).filter(
            LearningSession.user_id == user_id
        ).order_by(LearningSession.created_at.desc()).first()
        
        current_streak = current_session.streak_days if current_session else 0
        
        return {
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "average_score": round(avg_score, 2),
            "total_questions_answered": total_questions,
            "total_correct_answers": total_correct,
            "accuracy_percentage": round(accuracy, 2),
            "current_streak_days": current_streak,
            "completion_rate": round((completed_sessions / total_sessions * 100) if total_sessions > 0 else 0, 2)
        }

