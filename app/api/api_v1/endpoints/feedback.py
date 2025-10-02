"""
Feedback and survey API endpoints
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_postgres_session
from app.models.schemas import Feedback, FeedbackCreate, PaginatedResponse
from app.services.feedback_service import FeedbackService

router = APIRouter()


@router.get("/", response_model=PaginatedResponse)
async def get_feedback(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    student_id: Optional[int] = Query(None, description="Filter by student ID"),
    course_id: Optional[int] = Query(None, description="Filter by course ID"),
    feedback_type: Optional[str] = Query(None, description="Filter by feedback type"),
    rating_min: Optional[int] = Query(None, ge=1, le=5, description="Minimum rating"),
    rating_max: Optional[int] = Query(None, ge=1, le=5, description="Maximum rating"),
    db: Session = Depends(get_postgres_session)
):
    """Get paginated list of feedback with optional filtering"""
    feedback_service = FeedbackService(db)
    return await feedback_service.get_feedback_paginated(
        page=page, size=size, student_id=student_id, course_id=course_id,
        feedback_type=feedback_type, rating_min=rating_min, rating_max=rating_max
    )


@router.get("/{feedback_id}", response_model=Feedback)
async def get_feedback_by_id(
    feedback_id: str,
    db: Session = Depends(get_postgres_session)
):
    """Get feedback by ID"""
    feedback_service = FeedbackService(db)
    feedback = await feedback_service.get_feedback_by_id(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback


@router.post("/", response_model=Feedback)
async def create_feedback(
    feedback_data: FeedbackCreate,
    db: Session = Depends(get_postgres_session)
):
    """Create new feedback"""
    feedback_service = FeedbackService(db)
    return await feedback_service.create_feedback(feedback_data)


@router.get("/analytics/sentiment")
async def get_sentiment_analysis(
    student_id: Optional[int] = Query(None, description="Filter by student ID"),
    course_id: Optional[int] = Query(None, description="Filter by course ID"),
    feedback_type: Optional[str] = Query(None, description="Filter by feedback type"),
    start_date: Optional[str] = Query(None, description="Start date filter"),
    end_date: Optional[str] = Query(None, description="End date filter"),
    db: Session = Depends(get_postgres_session)
):
    """Get sentiment analysis of feedback"""
    feedback_service = FeedbackService(db)
    return await feedback_service.get_sentiment_analysis(
        student_id=student_id, course_id=course_id, feedback_type=feedback_type,
        start_date=start_date, end_date=end_date
    )


@router.get("/analytics/trends")
async def get_feedback_trends(
    student_id: Optional[int] = Query(None, description="Filter by student ID"),
    course_id: Optional[int] = Query(None, description="Filter by course ID"),
    period: str = Query("monthly", description="Trend period: daily, weekly, monthly"),
    db: Session = Depends(get_postgres_session)
):
    """Get feedback trends over time"""
    feedback_service = FeedbackService(db)
    return await feedback_service.get_feedback_trends(
        student_id=student_id, course_id=course_id, period=period
    )


@router.get("/analytics/ratings")
async def get_rating_distribution(
    student_id: Optional[int] = Query(None, description="Filter by student ID"),
    course_id: Optional[int] = Query(None, description="Filter by course ID"),
    feedback_type: Optional[str] = Query(None, description="Filter by feedback type"),
    db: Session = Depends(get_postgres_session)
):
    """Get rating distribution analysis"""
    feedback_service = FeedbackService(db)
    return await feedback_service.get_rating_distribution(
        student_id=student_id, course_id=course_id, feedback_type=feedback_type
    )


@router.get("/tags/popular")
async def get_popular_tags(
    limit: int = Query(20, ge=1, le=100, description="Number of tags to return"),
    db: Session = Depends(get_postgres_session)
):
    """Get most popular feedback tags"""
    feedback_service = FeedbackService(db)
    return await feedback_service.get_popular_tags(limit=limit)


@router.post("/bulk-import")
async def bulk_import_feedback(
    feedback_list: List[FeedbackCreate],
    db: Session = Depends(get_postgres_session)
):
    """Bulk import feedback data"""
    feedback_service = FeedbackService(db)
    return await feedback_service.bulk_import_feedback(feedback_list)
