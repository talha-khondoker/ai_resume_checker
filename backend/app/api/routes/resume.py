"""
Resume management API routes.
"""
from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException,
    status,
    Form
)
from sqlalchemy.orm import Session
from typing import List
import os
from app.db.database import get_db
from app.core.security import get_current_user
from app.core.config import settings
from app.models.models import Resume
from app.schemas.schemas import (
    ResumeUploadResponse,
    ResumeResponse,
    AnalysisRequest,
    AnalysisResponse,
    JobMatchRequest,
    JobMatchResponse
)
from app.services.resume_service import ResumeService, AnalysisService
from app.utils.file_handler import (
    validate_file,
    save_uploaded_file,
    extract_text_from_resume
)
from app.ml.analyzer import (
    extract_skills,
    calculate_job_match,
    semantic_similarity
)

router = APIRouter(prefix="/api/resume", tags=["Resume Management"])


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a resume file (PDF or DOCX).
    
    - **file**: Resume file (PDF or DOCX, max 10MB)
    """
    try:
        # Read file
        content = await file.read()
        
        # Validate file
        is_valid, error_msg = validate_file(file.filename, len(content))
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        
        # Save file
        file_path = save_uploaded_file(settings.UPLOAD_FOLDER, file.filename, content)
        
        # Extract text from resume
        extracted_text = extract_text_from_resume(file_path)
        
        # Create resume record
        resume = Resume(
            user_id=current_user["user_id"],
            filename=file.filename,
            file_path=file_path,
            extracted_text=extracted_text,
            is_processed=False
        )
        
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        return ResumeUploadResponse(
            id=resume.id,
            filename=resume.filename,
            file_path=resume.file_path,
            is_processed=resume.is_processed,
            created_at=resume.created_at
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File upload failed: {str(e)}"
        )


@router.get("/history", response_model=List[ResumeResponse])
async def get_resume_history(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get user's resume upload history."""
    resumes = ResumeService.get_user_resumes(db, current_user["user_id"])
    return resumes[skip:skip + limit]


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific resume details."""
    resume = ResumeService.get_resume(db, resume_id, current_user["user_id"])
    return resume


@router.delete("/{resume_id}")
async def delete_resume(
    resume_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a resume."""
    ResumeService.delete_resume(db, resume_id, current_user["user_id"])
    return {"message": "Resume deleted successfully"}


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    request: AnalysisRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze a resume for ATS score and quality metrics.
    
    - **resume_id**: ID of resume to analyze
    - **job_description**: Optional job description for matching
    - **analyze_type**: Type of analysis (full, ats, job-match)
    """
    # Get resume
    resume = ResumeService.get_resume(db, request.resume_id, current_user["user_id"])
    
    # Perform analysis
    analysis = AnalysisService.analyze_resume(
        db,
        resume,
        request.job_description
    )
    
    return analysis


@router.post("/job-match", response_model=JobMatchResponse)
async def match_with_job(
    request: JobMatchRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Match resume with a job description.
    
    - **resume_id**: ID of resume to match
    - **job_description**: Job description text (minimum 50 characters)
    """
    # Get resume
    resume = ResumeService.get_resume(db, request.resume_id, current_user["user_id"])
    
    if not resume.extracted_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume text not extracted yet"
        )
    
    # Extract skills
    resume_skills = extract_skills(resume.extracted_text)
    
    # Calculate match
    match_score, matching_skills, missing_skills = calculate_job_match(
        resume_skills,
        request.job_description
    )
    
    # Semantic similarity
    semantic_score = semantic_similarity(resume.extracted_text, request.job_description)
    
    # Combine scores
    combined_score = (match_score + semantic_score * 100) / 2
    
    # Create skill gaps
    job_skills = extract_skills(request.job_description)
    skill_gaps = []
    for skill in job_skills:
        if skill not in resume_skills:
            skill_gaps.append({
                "skill": skill,
                "importance": "critical" if skill in request.job_description[:500] else "high",
                "recommendation": f"Learn or improve {skill}"
            })
    
    # Recommendations
    recommendations = [
        f"Focus on acquiring these {len(missing_skills)} missing skills",
        "Highlight your matching skills in job applications",
        "Consider projects or learning to address skill gaps"
    ]
    
    return JobMatchResponse(
        match_score=combined_score,
        matching_skills=[
            {"skill": s, "match_percentage": 100, "relevance": "high"}
            for s in matching_skills
        ],
        missing_skills=missing_skills,
        skill_gaps=skill_gaps,
        recommendations=recommendations
    )
