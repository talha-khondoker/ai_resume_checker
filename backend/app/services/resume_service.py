"""
Resume analysis service for analyzing resumes and matching with jobs.
"""
import json
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.models import Resume, ResumeData, AnalysisReport
from app.ml.analyzer import (
    extract_skills,
    extract_emails,
    extract_phones,
    extract_name,
    extract_education,
    extract_experience,
    calculate_ats_score,
    calculate_job_match,
    generate_improvement_suggestions,
    recommend_roles,
    semantic_similarity
)
from app.utils.file_handler import clean_text


class ResumeService:
    """Service for resume operations."""
    
    @staticmethod
    def get_resume(db: Session, resume_id: int, user_id: int) -> Resume:
        """Get resume by ID and verify ownership."""
        resume = db.query(Resume).filter(
            Resume.id == resume_id,
            Resume.user_id == user_id
        ).first()
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        
        return resume
    
    @staticmethod
    def get_user_resumes(db: Session, user_id: int) -> List[Resume]:
        """Get all resumes for a user."""
        return db.query(Resume).filter(
            Resume.user_id == user_id
        ).order_by(Resume.created_at.desc()).all()
    
    @staticmethod
    def delete_resume(db: Session, resume_id: int, user_id: int) -> bool:
        """Delete a resume."""
        resume = ResumeService.get_resume(db, resume_id, user_id)
        
        # Delete file if exists
        import os
        if os.path.exists(resume.file_path):
            os.remove(resume.file_path)
        
        db.delete(resume)
        db.commit()
        return True


class AnalysisService:
    """Service for resume analysis operations."""
    
    @staticmethod
    def analyze_resume(
        db: Session,
        resume: Resume,
        job_description: Optional[str] = None
    ) -> AnalysisReport:
        """
        Analyze a resume and optionally match with job description.
        
        Args:
            db: Database session
            resume: Resume object
            job_description: Optional job description for matching
        
        Returns:
            AnalysisReport object
        """
        # Extract text and clean
        extracted_text = resume.extracted_text or ""
        cleaned_text = clean_text(extracted_text)
        
        # Extract information
        skills = extract_skills(extracted_text)
        emails = extract_emails(extracted_text)
        phones = extract_phones(extracted_text)
        name = extract_name(extracted_text)
        education = extract_education(extracted_text)
        experience = extract_experience(extracted_text)
        
        # Calculate ATS score
        ats_score = calculate_ats_score(extracted_text, skills)
        
        # Determine resume strength
        if ats_score >= 80:
            resume_strength = "strong"
        elif ats_score >= 60:
            resume_strength = "moderate"
        else:
            resume_strength = "weak"
        
        # Generate suggestions
        suggestions = generate_improvement_suggestions(
            extracted_text,
            ats_score,
            skills
        )
        
        # Recommend roles
        recommended_roles = recommend_roles(skills)
        
        # Job matching if description provided
        match_score = None
        matching_skills = []
        missing_skills = []
        skill_gaps = []
        
        if job_description:
            match_score_val, matching_skills, missing_skills = calculate_job_match(
                skills,
                job_description
            )
            match_score = match_score_val
            
            # Semantic similarity for additional insight
            semantic_score = semantic_similarity(
                extracted_text,
                job_description
            )
            # Combine keyword and semantic matching
            if match_score is not None:
                match_score = (match_score + semantic_score * 100) / 2
            
            # Create skill gap analysis
            job_skills = extract_skills(job_description)
            for skill in job_skills:
                if skill not in skills:
                    skill_gaps.append({
                        "skill": skill,
                        "importance": "critical" if skill in job_description[:500] else "high",
                        "recommendation": f"Learn or improve {skill}"
                    })
        
        # Save extracted data
        resume_data = ResumeData(
            resume_id=resume.id,
            name=name,
            email=emails[0] if emails else None,
            phone=phones[0] if phones else None,
            skills=json.dumps(skills),
            education=json.dumps(education),
            experience=json.dumps(experience),
            summary=extracted_text[:500] if extracted_text else None
        )
        db.add(resume_data)
        
        # Create analysis report
        analysis = AnalysisReport(
            resume_id=resume.id,
            job_description=job_description,
            match_score=match_score,
            matching_skills=json.dumps([
                {"skill": s, "match_percentage": 100, "relevance": "high"}
                for s in matching_skills
            ]),
            missing_skills=json.dumps(missing_skills),
            suggestions=json.dumps(suggestions),
            skill_gap_analysis=json.dumps(skill_gaps),
            recommended_roles=json.dumps(recommended_roles),
            resume_strength=resume_strength,
            grammar_feedback="Resume structure appears to be standard"
        )
        db.add(analysis)
        
        # Update resume with ATS score
        resume.ats_score = ats_score
        resume.is_processed = True
        
        db.commit()
        db.refresh(analysis)
        
        return analysis
    
    @staticmethod
    def get_analysis_report(
        db: Session,
        report_id: int,
        user_id: int
    ) -> AnalysisReport:
        """Get analysis report and verify ownership."""
        report = db.query(AnalysisReport).join(Resume).filter(
            AnalysisReport.id == report_id,
            Resume.user_id == user_id
        ).first()
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis report not found"
            )
        
        return report
    
    @staticmethod
    def get_resume_analysis_history(
        db: Session,
        resume_id: int,
        user_id: int
    ) -> List[AnalysisReport]:
        """Get analysis history for a resume."""
        return db.query(AnalysisReport).join(Resume).filter(
            AnalysisReport.resume_id == resume_id,
            Resume.user_id == user_id
        ).order_by(AnalysisReport.created_at.desc()).all()
