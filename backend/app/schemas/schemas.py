"""
Pydantic schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# ===================== Auth Schemas =====================

class UserBase(BaseModel):
    """Base user schema."""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr


class UserCreate(UserBase):
    """User creation schema."""
    password: str = Field(..., min_length=8, max_length=255)


class UserLogin(BaseModel):
    """User login schema."""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """User response schema."""
    id: int
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int


# ===================== Resume Schemas =====================

class ResumeData(BaseModel):
    """Extracted resume data schema."""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: Optional[List[str]] = []
    education: Optional[List[dict]] = []
    experience: Optional[List[dict]] = []
    certifications: Optional[List[str]] = []
    projects: Optional[List[dict]] = []
    summary: Optional[str] = None


class ResumeUploadResponse(BaseModel):
    """Resume upload response schema."""
    id: int
    filename: str
    file_path: str
    is_processed: bool
    created_at: datetime


class ResumeResponse(ResumeUploadResponse):
    """Resume response schema."""
    ats_score: Optional[float] = None
    extracted_text: Optional[str] = None
    
    class Config:
        from_attributes = True


# ===================== Analysis Schemas =====================

class MatchingSkills(BaseModel):
    """Matching skills schema."""
    skill: str
    match_percentage: float
    relevance: str  # high, medium, low


class SkillGap(BaseModel):
    """Skill gap analysis schema."""
    skill: str
    importance: str  # critical, high, medium, low
    recommendation: str


class AnalysisRequest(BaseModel):
    """Analysis request schema."""
    resume_id: int
    job_description: Optional[str] = None
    analyze_type: str = "full"  # full, ats, job-match


class AnalysisResponse(BaseModel):
    """Analysis response schema."""
    id: int
    resume_id: int
    ats_score: Optional[float] = None
    match_score: Optional[float] = None
    matching_skills: List[MatchingSkills] = []
    missing_skills: List[str] = []
    skill_gaps: List[SkillGap] = []
    suggestions: List[str] = []
    grammar_feedback: Optional[str] = None
    resume_strength: Optional[str] = None
    recommended_roles: List[str] = []
    created_at: datetime
    
    class Config:
        from_attributes = True


class JobMatchRequest(BaseModel):
    """Job matching request schema."""
    resume_id: int
    job_description: str = Field(..., min_length=50)


class JobMatchResponse(BaseModel):
    """Job matching response schema."""
    match_score: float = Field(..., ge=0, le=100)
    matching_skills: List[MatchingSkills]
    missing_skills: List[str]
    skill_gaps: List[SkillGap]
    recommendations: List[str]


# ===================== Admin Schemas =====================

class UserStatsResponse(BaseModel):
    """User statistics response schema."""
    total_users: int
    active_users: int
    total_resumes: int
    average_ats_score: Optional[float] = None


class AdminReportResponse(BaseModel):
    """Admin report response schema."""
    user_id: int
    email: str
    resumes_count: int
    average_ats_score: Optional[float] = None
    last_upload: Optional[datetime] = None
