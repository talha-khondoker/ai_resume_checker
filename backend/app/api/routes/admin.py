"""
Admin API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.db.database import get_db
from app.core.security import get_current_admin_user
from app.models.models import User, Resume, AnalysisReport, UserRole
from app.schemas.schemas import (
    UserStatsResponse,
    AdminReportResponse
)

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/stats", response_model=UserStatsResponse)
async def get_statistics(
    current_user: dict = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get system statistics."""
    total_users = db.query(func.count(User.id)).scalar()
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()
    total_resumes = db.query(func.count(Resume.id)).scalar()
    
    avg_ats = db.query(func.avg(Resume.ats_score)).filter(
        Resume.ats_score != None
    ).scalar()
    
    return UserStatsResponse(
        total_users=total_users or 0,
        active_users=active_users or 0,
        total_resumes=total_resumes or 0,
        average_ats_score=float(avg_ats) if avg_ats else None
    )


@router.get("/users", response_model=List[AdminReportResponse])
async def get_users_report(
    current_user: dict = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get report of all users and their resume statistics."""
    users = db.query(User).offset(skip).limit(limit).all()
    
    reports = []
    for user in users:
        resume_count = db.query(func.count(Resume.id)).filter(
            Resume.user_id == user.id
        ).scalar()
        
        avg_ats = db.query(func.avg(Resume.ats_score)).filter(
            Resume.user_id == user.id,
            Resume.ats_score != None
        ).scalar()
        
        last_upload = db.query(Resume.created_at).filter(
            Resume.user_id == user.id
        ).order_by(Resume.created_at.desc()).first()
        
        reports.append(AdminReportResponse(
            user_id=user.id,
            email=user.email,
            resumes_count=resume_count or 0,
            average_ats_score=float(avg_ats) if avg_ats else None,
            last_upload=last_upload[0] if last_upload else None
        ))
    
    return reports


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: dict = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a user and all associated data."""
    # Prevent self-deletion
    if current_user["user_id"] == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    
    return {"message": f"User {user_id} deleted successfully"}


@router.get("/resumes", response_model=List)
async def get_all_resumes(
    current_user: dict = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get all resumes in the system."""
    resumes = db.query(Resume).offset(skip).limit(limit).all()
    return resumes


@router.delete("/resumes/{resume_id}")
async def delete_resume(
    resume_id: int,
    current_user: dict = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a resume (admin only)."""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Delete file
    import os
    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)
    
    db.delete(resume)
    db.commit()
    
    return {"message": f"Resume {resume_id} deleted successfully"}
