"""
AI/ML utilities for resume analysis.
"""
import json
import re
from typing import List, Dict, Tuple, Optional
import numpy as np
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from app.core.config import settings


# Load spacy model
try:
    nlp = spacy.load(settings.SPACY_MODEL)
except OSError:
    import subprocess
    subprocess.run([
        "python", "-m", "spacy", "download", settings.SPACY_MODEL
    ], check=False)
    nlp = spacy.load(settings.SPACY_MODEL)

# Load sentence transformer
model = SentenceTransformer('all-MiniLM-L6-v2')


# ===================== Text Extraction =====================

def extract_emails(text: str) -> List[str]:
    """Extract email addresses from text."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)


def extract_phones(text: str) -> List[str]:
    """Extract phone numbers from text."""
    phone_pattern = r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}'
    return re.findall(phone_pattern, text)


def extract_name(text: str) -> Optional[str]:
    """
    Extract name from resume.
    Usually appears at the beginning.
    """
    doc = nlp(text[:500])  # Process only first 500 chars
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None


# ===================== Skill Extraction =====================

TECHNICAL_SKILLS = {
    # Programming Languages
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php',
    'ruby', 'golang', 'rust', 'scala', 'kotlin', 'swift', 'objective-c',
    
    # Web Frameworks
    'react', 'angular', 'vue', 'django', 'flask', 'fastapi', 'spring',
    'express', 'node', 'nextjs', 'gatsby', 'svelte',
    
    # Databases
    'postgresql', 'mysql', 'mongodb', 'redis', 'cassandra', 'dynamodb',
    'elasticsearch', 'firebase', 'oracle', 'sqlserver',
    
    # Cloud & DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'circleci',
    'github', 'gitlab', 'bitbucket', 'terraform', 'ansible',
    
    # Data Science & ML
    'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
    'matplotlib', 'seaborn', 'jupyter', 'spark', 'hadoop',
    
    # Tools
    'git', 'linux', 'windows', 'macos', 'jira', 'confluence', 'slack',
    'figma', 'sketch', 'photoshop', 'illustrator', 'blender',
    
    # Soft Skills (common in resumes)
    'leadership', 'communication', 'teamwork', 'problem-solving',
    'project management', 'agile', 'scrum', 'oop', 'rest', 'graphql',
    'microservices', 'testing', 'ci/cd'
}


def extract_skills(text: str) -> List[str]:
    """
    Extract technical skills from resume text.
    
    Args:
        text: Resume text
    
    Returns:
        List of skills found
    """
    text_lower = text.lower()
    skills = []
    
    # Direct skill matching
    for skill in TECHNICAL_SKILLS:
        # Use word boundaries to avoid partial matches
        pattern = rf'\b{re.escape(skill)}\b'
        if re.search(pattern, text_lower):
            skills.append(skill)
    
    # Also check for common multi-word skills
    multi_word_skills = {
        'machine learning': 'Machine Learning',
        'deep learning': 'Deep Learning',
        'natural language processing': 'NLP',
        'computer vision': 'Computer Vision',
        'data science': 'Data Science',
        'web development': 'Web Development',
        'mobile development': 'Mobile Development',
        'full stack': 'Full Stack',
        'front end': 'Frontend',
        'back end': 'Backend'
    }
    
    for skill_phrase, skill_name in multi_word_skills.items():
        if skill_phrase in text_lower:
            skills.append(skill_name)
    
    return list(set(skills))  # Remove duplicates


def extract_education(text: str) -> List[Dict]:
    """
    Extract education information.
    
    Args:
        text: Resume text
    
    Returns:
        List of education entries
    """
    education = []
    doc = nlp(text)
    
    # Common degree patterns
    degree_patterns = [
        r'bachelor',
        r'master',
        r'phd',
        r'bs',
        r'ms',
        r'ba',
        r'ma',
        r'diploma',
        r'associate'
    ]
    
    # Look for degree mentions
    for ent in doc.ents:
        if ent.label_ == "ORG":  # Organization (often universities)
            # Check nearby text for degrees
            span_text = text[max(0, ent.start_char - 100):ent.end_char + 100].lower()
            degree = None
            for pattern in degree_patterns:
                if re.search(pattern, span_text):
                    degree = pattern
                    break
            
            if degree:
                education.append({
                    "institution": ent.text,
                    "degree": degree
                })
    
    return education


def extract_experience(text: str) -> List[Dict]:
    """
    Extract work experience.
    
    Args:
        text: Resume text
    
    Returns:
        List of experience entries
    """
    experience = []
    
    # Simple pattern for work experience section
    exp_section = text.split('experience', 1)[-1] if 'experience' in text.lower() else ""
    
    # Split by job entries (usually separated by multiple newlines or bullets)
    jobs = re.split(r'\n\n+|\n\s*[-•]\s*', exp_section)
    
    for job in jobs[:10]:  # Limit to 10 entries
        if len(job.strip()) > 20:
            experience.append({
                "description": job.strip()[:200]  # First 200 chars
            })
    
    return experience


# ===================== ATS Score Calculation =====================

def calculate_ats_score(
    resume_text: str,
    extracted_skills: List[str]
) -> float:
    """
    Calculate ATS (Applicant Tracking System) compatibility score.
    
    Factors:
    - Text extraction success
    - Keyword density
    - Skill presence
    - Standard formatting
    
    Args:
        resume_text: Extracted resume text
        extracted_skills: List of skills found
    
    Returns:
        ATS score (0-100)
    """
    score = 0.0
    
    # Text quality (20 points)
    if len(resume_text) > 200:
        score += 20
    
    # Keyword diversity (20 points)
    word_count = len(resume_text.split())
    if word_count > 300:
        score += 20
    
    # Skills presence (20 points)
    if len(extracted_skills) >= 5:
        score += 20
    elif len(extracted_skills) >= 3:
        score += 15
    elif len(extracted_skills) > 0:
        score += 10
    
    # Standard format indicators (20 points)
    format_indicators = [
        'experience' in resume_text.lower(),
        'education' in resume_text.lower(),
        'skills' in resume_text.lower(),
        'email' in resume_text.lower() or '@' in resume_text
    ]
    score += len([ind for ind in format_indicators if ind]) * 5
    
    # Common quality indicators (20 points)
    quality_indicators = [
        len(extract_phones(resume_text)) > 0,
        len(extract_emails(resume_text)) > 0,
        resume_text.count('\n') > 5,  # Good structure
    ]
    score += len([ind for ind in quality_indicators if ind]) * 6.67
    
    return min(100.0, score)


# ===================== Job Matching =====================

def calculate_job_match(
    resume_skills: List[str],
    job_description: str
) -> Tuple[float, List[str], List[str]]:
    """
    Calculate resume-job match score.
    
    Args:
        resume_skills: Skills from resume
        job_description: Job description text
    
    Returns:
        Tuple of (match_score, matching_skills, missing_skills)
    """
    job_skills = extract_skills(job_description)
    
    matching = [skill for skill in resume_skills if skill in job_skills]
    missing = [skill for skill in job_skills if skill not in resume_skills]
    
    if len(job_skills) == 0:
        match_score = 0.0
    else:
        match_score = (len(matching) / len(job_skills)) * 100
    
    return match_score, matching, missing


def semantic_similarity(text1: str, text2: str) -> float:
    """
    Calculate semantic similarity between two texts using embeddings.
    
    Args:
        text1: First text
        text2: Second text
    
    Returns:
        Similarity score (0-1)
    """
    # Truncate long texts to avoid memory issues
    text1 = text1[:1000]
    text2 = text2[:1000]
    
    # Get embeddings
    embeddings = model.encode([text1, text2])
    
    # Calculate cosine similarity
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    
    return float(similarity)


# ===================== Recommendations =====================

def generate_improvement_suggestions(
    resume_text: str,
    ats_score: float,
    extracted_skills: List[str]
) -> List[str]:
    """
    Generate improvement suggestions for resume.
    
    Args:
        resume_text: Resume text
        ats_score: Current ATS score
        extracted_skills: Extracted skills
    
    Returns:
        List of suggestions
    """
    suggestions = []
    
    # ATS-based suggestions
    if ats_score < 50:
        suggestions.append("Improve resume formatting and structure for better ATS compatibility")
        suggestions.append("Ensure you have clear sections: Summary, Experience, Education, Skills")
    
    if 'summary' not in resume_text.lower():
        suggestions.append("Add a professional summary at the top of your resume")
    
    if 'objective' not in resume_text.lower() and 'summary' not in resume_text.lower():
        suggestions.append("Include a career objective or professional summary")
    
    # Skill-based suggestions
    if len(extracted_skills) < 5:
        suggestions.append("Add more technical skills to increase resume visibility")
    
    if 'certification' not in resume_text.lower():
        suggestions.append("Consider adding relevant certifications to strengthen your profile")
    
    # Content suggestions
    word_count = len(resume_text.split())
    if word_count < 300:
        suggestions.append("Expand your resume with more detailed descriptions of your experience")
    elif word_count > 1000:
        suggestions.append("Consider condensing your resume - aim for 300-800 words")
    
    return suggestions


JOB_ROLES_KEYWORDS = {
    'Software Engineer': ['python', 'java', 'c++', 'javascript', 'algorithm', 'database'],
    'Data Scientist': ['python', 'machine learning', 'tensorflow', 'pandas', 'scikit-learn'],
    'Frontend Developer': ['react', 'javascript', 'css', 'html', 'typescript', 'vue'],
    'DevOps Engineer': ['docker', 'kubernetes', 'aws', 'ci/cd', 'terraform', 'jenkins'],
    'Product Manager': ['agile', 'scrum', 'roadmap', 'analytics', 'product strategy'],
    'ML Engineer': ['tensorflow', 'pytorch', 'deep learning', 'gpu', 'computer vision'],
    'Cloud Architect': ['aws', 'azure', 'gcp', 'kubernetes', 'microservices', 'terraform'],
}


def recommend_roles(extracted_skills: List[str]) -> List[str]:
    """
    Recommend job roles based on skills.
    
    Args:
        extracted_skills: List of skills from resume
    
    Returns:
        List of recommended roles
    """
    skills_lower = [s.lower() for s in extracted_skills]
    role_scores = {}
    
    for role, keywords in JOB_ROLES_KEYWORDS.items():
        match_count = sum(1 for kw in keywords if any(kw in s for s in skills_lower))
        if match_count > 0:
            role_scores[role] = match_count
    
    # Sort by match count and return top 3
    top_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    return [role for role, _ in top_roles]
