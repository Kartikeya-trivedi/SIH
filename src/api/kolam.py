from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from datetime import datetime

from src.core.database import get_db
from src.core.security import verify_token
from src.schemas import (
    KolamImage, KolamImageCreate, KolamImageUpdate, 
    GeneratedKolam, GeneratedKolamCreate, GeneratedKolamUpdate,
    KolamImageAnalysis
)
from src.services.kolam_service import KolamService
from src.services.ai.detection_service import DetectionService
from src.services.ai.generation_service import GenerationService

router = APIRouter()


def get_current_user_id(token: str = Depends(verify_token)) -> int:
    """Extract user ID from JWT token."""
    # This is a simplified version - in a real app, you'd decode the token properly
    # For now, we'll assume the token contains user info
    return 1  # Placeholder


@router.post("/upload", response_model=KolamImage)
async def upload_kolam_image(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    is_public: bool = Form(False),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Upload a Kolam image for analysis."""
    kolam_service = KolamService(db)
    
    # Validate file
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Save file
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
    filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join("uploads", filename)
    
    os.makedirs("uploads", exist_ok=True)
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Create database record
    kolam_data = KolamImageCreate(
        title=title,
        description=description,
        tags=tags.split(',') if tags else None,
        is_public=is_public
    )
    
    kolam_image = kolam_service.create_kolam_image(
        user_id=current_user_id,
        filename=filename,
        file_path=file_path,
        file_size=len(content),
        mime_type=file.content_type,
        kolam_data=kolam_data
    )
    
    return kolam_image


@router.post("/analyze/{image_id}", response_model=KolamImageAnalysis)
async def analyze_kolam_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Analyze a Kolam image using AI."""
    kolam_service = KolamService(db)
    detection_service = DetectionService()
    
    # Get image from database
    kolam_image = kolam_service.get_kolam_image(image_id, current_user_id)
    if not kolam_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kolam image not found"
        )
    
    # Perform AI analysis
    analysis = await detection_service.analyze_image(kolam_image.file_path)
    
    # Update database with analysis results
    kolam_service.update_kolam_analysis(image_id, analysis)
    
    return analysis


@router.get("/images", response_model=List[KolamImage])
async def get_user_kolam_images(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Get user's Kolam images."""
    kolam_service = KolamService(db)
    images = kolam_service.get_user_kolam_images(current_user_id, skip=skip, limit=limit)
    return images


@router.get("/images/{image_id}", response_model=KolamImage)
async def get_kolam_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Get a specific Kolam image."""
    kolam_service = KolamService(db)
    image = kolam_service.get_kolam_image(image_id, current_user_id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kolam image not found"
        )
    return image


@router.put("/images/{image_id}", response_model=KolamImage)
async def update_kolam_image(
    image_id: int,
    image_update: KolamImageUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Update Kolam image metadata."""
    kolam_service = KolamService(db)
    
    image = kolam_service.get_kolam_image(image_id, current_user_id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kolam image not found"
        )
    
    updated_image = kolam_service.update_kolam_image(image_id, image_update)
    return updated_image


@router.delete("/images/{image_id}")
async def delete_kolam_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Delete a Kolam image."""
    kolam_service = KolamService(db)
    
    image = kolam_service.get_kolam_image(image_id, current_user_id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kolam image not found"
        )
    
    # Delete file
    if os.path.exists(image.file_path):
        os.remove(image.file_path)
    
    # Delete database record
    kolam_service.delete_kolam_image(image_id)
    
    return {"message": "Kolam image deleted successfully"}


# Generated Kolam endpoints
@router.post("/generate", response_model=GeneratedKolam)
async def generate_kolam(
    generation_data: GeneratedKolamCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Generate a new Kolam pattern using AI."""
    kolam_service = KolamService(db)
    generation_service = GenerationService()
    
    # Generate Kolam pattern
    generated_pattern = await generation_service.generate_pattern(
        pattern_type=generation_data.pattern_type,
        complexity_level=generation_data.complexity_level,
        symmetry_type=generation_data.symmetry_type,
        size=generation_data.size
    )
    
    # Save generated pattern
    generated_kolam = kolam_service.create_generated_kolam(
        user_id=current_user_id,
        generation_data=generation_data,
        svg_data=generated_pattern["svg_data"],
        image_path=generated_pattern["image_path"]
    )
    
    return generated_kolam


@router.get("/generated", response_model=List[GeneratedKolam])
async def get_generated_kolams(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Get user's generated Kolam patterns."""
    kolam_service = KolamService(db)
    generated_kolams = kolam_service.get_user_generated_kolams(
        current_user_id, skip=skip, limit=limit
    )
    return generated_kolams


@router.get("/generated/{kolam_id}", response_model=GeneratedKolam)
async def get_generated_kolam(
    kolam_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Get a specific generated Kolam pattern."""
    kolam_service = KolamService(db)
    kolam = kolam_service.get_generated_kolam(kolam_id, current_user_id)
    if not kolam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Generated Kolam not found"
        )
    return kolam


@router.put("/generated/{kolam_id}", response_model=GeneratedKolam)
async def update_generated_kolam(
    kolam_id: int,
    kolam_update: GeneratedKolamUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Update generated Kolam metadata."""
    kolam_service = KolamService(db)
    
    kolam = kolam_service.get_generated_kolam(kolam_id, current_user_id)
    if not kolam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Generated Kolam not found"
        )
    
    updated_kolam = kolam_service.update_generated_kolam(kolam_id, kolam_update)
    return updated_kolam

