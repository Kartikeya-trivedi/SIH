from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from datetime import datetime

from src.db.models.models import KolamImage, GeneratedKolam
from src.schemas import (
    KolamImageCreate, KolamImageUpdate, GeneratedKolamCreate, GeneratedKolamUpdate,
    KolamImageAnalysis
)
from src.core.logging import LoggerMixin


class KolamService(LoggerMixin):
    """Service for Kolam-related operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Kolam Image operations
    def create_kolam_image(
        self, 
        user_id: int, 
        filename: str, 
        file_path: str, 
        file_size: int, 
        mime_type: str,
        kolam_data: KolamImageCreate
    ) -> KolamImage:
        """Create a new Kolam image record."""
        db_kolam = KolamImage(
            user_id=user_id,
            filename=filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=mime_type,
            title=kolam_data.title,
            description=kolam_data.description,
            tags=kolam_data.tags,
            is_public=kolam_data.is_public
        )
        self.db.add(db_kolam)
        self.db.commit()
        self.db.refresh(db_kolam)
        
        self.logger.info("Kolam image created", image_id=db_kolam.id, user_id=user_id)
        return db_kolam
    
    def get_kolam_image(self, image_id: int, user_id: int) -> Optional[KolamImage]:
        """Get Kolam image by ID for a specific user."""
        return self.db.query(KolamImage).filter(
            and_(KolamImage.id == image_id, KolamImage.user_id == user_id)
        ).first()
    
    def get_user_kolam_images(
        self, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[KolamImage]:
        """Get user's Kolam images."""
        return self.db.query(KolamImage).filter(
            KolamImage.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def update_kolam_image(
        self, 
        image_id: int, 
        image_update: KolamImageUpdate
    ) -> Optional[KolamImage]:
        """Update Kolam image metadata."""
        db_kolam = self.db.query(KolamImage).filter(KolamImage.id == image_id).first()
        if not db_kolam:
            return None
        
        update_data = image_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_kolam, field, value)
        
        db_kolam.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_kolam)
        
        self.logger.info("Kolam image updated", image_id=image_id)
        return db_kolam
    
    def update_kolam_analysis(
        self, 
        image_id: int, 
        analysis: KolamImageAnalysis
    ) -> Optional[KolamImage]:
        """Update Kolam image with AI analysis results."""
        db_kolam = self.db.query(KolamImage).filter(KolamImage.id == image_id).first()
        if not db_kolam:
            return None
        
        db_kolam.detected_patterns = analysis.detected_patterns
        db_kolam.confidence_scores = analysis.confidence_scores
        db_kolam.complexity_score = analysis.complexity_score
        db_kolam.symmetry_type = analysis.symmetry_type
        db_kolam.geometric_features = analysis.geometric_features
        db_kolam.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_kolam)
        
        self.logger.info("Kolam analysis updated", image_id=image_id)
        return db_kolam
    
    def delete_kolam_image(self, image_id: int) -> bool:
        """Delete a Kolam image."""
        db_kolam = self.db.query(KolamImage).filter(KolamImage.id == image_id).first()
        if not db_kolam:
            return False
        
        self.db.delete(db_kolam)
        self.db.commit()
        
        self.logger.info("Kolam image deleted", image_id=image_id)
        return True
    
    # Generated Kolam operations
    def create_generated_kolam(
        self,
        user_id: int,
        generation_data: GeneratedKolamCreate,
        svg_data: str,
        image_path: str
    ) -> GeneratedKolam:
        """Create a new generated Kolam record."""
        db_kolam = GeneratedKolam(
            user_id=user_id,
            pattern_type=generation_data.pattern_type,
            complexity_level=generation_data.complexity_level,
            symmetry_type=generation_data.symmetry_type,
            size=generation_data.size,
            title=generation_data.title,
            description=generation_data.description,
            svg_data=svg_data,
            image_path=image_path,
            generation_params=generation_data.generation_params
        )
        self.db.add(db_kolam)
        self.db.commit()
        self.db.refresh(db_kolam)
        
        self.logger.info("Generated Kolam created", kolam_id=db_kolam.id, user_id=user_id)
        return db_kolam
    
    def get_generated_kolam(self, kolam_id: int, user_id: int) -> Optional[GeneratedKolam]:
        """Get generated Kolam by ID for a specific user."""
        return self.db.query(GeneratedKolam).filter(
            and_(GeneratedKolam.id == kolam_id, GeneratedKolam.user_id == user_id)
        ).first()
    
    def get_user_generated_kolams(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[GeneratedKolam]:
        """Get user's generated Kolam patterns."""
        return self.db.query(GeneratedKolam).filter(
            GeneratedKolam.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def update_generated_kolam(
        self,
        kolam_id: int,
        kolam_update: GeneratedKolamUpdate
    ) -> Optional[GeneratedKolam]:
        """Update generated Kolam metadata."""
        db_kolam = self.db.query(GeneratedKolam).filter(GeneratedKolam.id == kolam_id).first()
        if not db_kolam:
            return None
        
        update_data = kolam_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_kolam, field, value)
        
        self.db.commit()
        self.db.refresh(db_kolam)
        
        self.logger.info("Generated Kolam updated", kolam_id=kolam_id)
        return db_kolam
    
    def delete_generated_kolam(self, kolam_id: int) -> bool:
        """Delete a generated Kolam."""
        db_kolam = self.db.query(GeneratedKolam).filter(GeneratedKolam.id == kolam_id).first()
        if not db_kolam:
            return False
        
        self.db.delete(db_kolam)
        self.db.commit()
        
        self.logger.info("Generated Kolam deleted", kolam_id=kolam_id)
        return True

