"""
SQLAlchemy database models.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.database import Base


class UserRole(str, enum.Enum):
    """User roles enumeration."""
    USER = "user"
    ADMIN = "admin"


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email}>"


class Resume(Base):
    """Resume model."""
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    extracted_text = Column(Text, nullable=True)
    ats_score = Column(Float, nullable=True)
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="resumes")
    analysis_reports = relationship("AnalysisReport", back_populates="resume", cascade="all, delete-orphan")
    extracted_data = relationship("ResumeData", back_populates="resume", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Resume {self.filename}>"


class ResumeData(Base):
    """Extracted resume data model."""
    __tablename__ = "resume_data"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    skills = Column(Text, nullable=True)  # JSON string
    education = Column(Text, nullable=True)  # JSON string
    experience = Column(Text, nullable=True)  # JSON string
    certifications = Column(Text, nullable=True)  # JSON string
    projects = Column(Text, nullable=True)  # JSON string
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    resume = relationship("Resume", back_populates="extracted_data")
    
    def __repr__(self):
        return f"<ResumeData {self.resume_id}>"


class AnalysisReport(Base):
    """Analysis report model."""
    __tablename__ = "analysis_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_description = Column(Text, nullable=True)
    match_score = Column(Float, nullable=True)
    matching_skills = Column(Text, nullable=True)  # JSON string
    missing_skills = Column(Text, nullable=True)  # JSON string
    suggestions = Column(Text, nullable=True)  # JSON string
    grammar_feedback = Column(Text, nullable=True)
    skill_gap_analysis = Column(Text, nullable=True)  # JSON string
    recommended_roles = Column(Text, nullable=True)  # JSON string
    resume_strength = Column(String(50), nullable=True)  # weak, moderate, strong
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    resume = relationship("Resume", back_populates="analysis_reports")
    
    def __repr__(self):
        return f"<AnalysisReport {self.id}>"
