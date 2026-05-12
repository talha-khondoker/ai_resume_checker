"""
Health check endpoint for monitoring
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint for monitoring and load balancers
    Returns application and database status
    """
    try:
        # Check database connection
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "database": db_status,
        "service": "AI Resume Analyzer API"
    }


@router.get("/health/ready")
async def readiness_check(db: Session = Depends(get_db)):
    """Kubernetes readiness probe"""
    try:
        db.execute("SELECT 1")
        return {"ready": True}
    except Exception:
        return {"ready": False}


@router.get("/health/live")
async def liveness_check():
    """Kubernetes liveness probe"""
    return {"alive": True}
