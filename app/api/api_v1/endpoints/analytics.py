"""
Analytics and reporting API endpoints
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.db.database import get_postgres_session
from app.models.schemas import (
    PerformanceMetrics, EnrollmentStats, CourseStats, 
    DepartmentStats, DashboardData
)
from app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/performance", response_model=List[PerformanceMetrics])
async def get_performance_metrics(
    student_id: Optional[int] = Query(None, description="Filter by student ID"),
    course_id: Optional[int] = Query(None, description="Filter by course ID"),
    start_date: Optional[date] = Query(None, description="Start date filter"),
    end_date: Optional[date] = Query(None, description="End date filter"),
    db: Session = Depends(get_postgres_session)
):
    """Get student performance metrics"""
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_performance_metrics(
        student_id=student_id,
        course_id=course_id,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/enrollment", response_model=EnrollmentStats)
async def get_enrollment_stats(
    start_date: Optional[date] = Query(None, description="Start date filter"),
    end_date: Optional[date] = Query(None, description="End date filter"),
    department_id: Optional[int] = Query(None, description="Filter by department"),
    db: Session = Depends(get_postgres_session)
):
    """Get enrollment statistics"""
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_enrollment_stats(
        start_date=start_date,
        end_date=end_date,
        department_id=department_id
    )


@router.get("/courses", response_model=List[CourseStats])
async def get_course_stats(
    department_id: Optional[int] = Query(None, description="Filter by department"),
    level: Optional[str] = Query(None, description="Filter by course level"),
    start_date: Optional[date] = Query(None, description="Start date filter"),
    end_date: Optional[date] = Query(None, description="End date filter"),
    db: Session = Depends(get_postgres_session)
):
    """Get course statistics"""
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_course_stats(
        department_id=department_id,
        level=level,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/departments", response_model=List[DepartmentStats])
async def get_department_stats(
    start_date: Optional[date] = Query(None, description="Start date filter"),
    end_date: Optional[date] = Query(None, description="End date filter"),
    db: Session = Depends(get_postgres_session)
):
    """Get department statistics"""
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_department_stats(
        start_date=start_date,
        end_date=end_date
    )


@router.get("/dashboard", response_model=DashboardData)
async def get_dashboard_data(
    start_date: Optional[date] = Query(None, description="Start date filter"),
    end_date: Optional[date] = Query(None, description="End date filter"),
    department_id: Optional[int] = Query(None, description="Filter by department"),
    db: Session = Depends(get_postgres_session)
):
    """Get comprehensive dashboard data"""
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_dashboard_data(
        start_date=start_date,
        end_date=end_date,
        department_id=department_id
    )


@router.get("/trends/performance")
async def get_performance_trends(
    student_id: Optional[int] = Query(None, description="Filter by student ID"),
    course_id: Optional[int] = Query(None, description="Filter by course ID"),
    period: str = Query("monthly", description="Trend period: daily, weekly, monthly, yearly"),
    db: Session = Depends(get_postgres_session)
):
    """Get performance trends over time"""
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_performance_trends(
        student_id=student_id,
        course_id=course_id,
        period=period
    )


@router.get("/trends/enrollment")
async def get_enrollment_trends(
    department_id: Optional[int] = Query(None, description="Filter by department"),
    period: str = Query("monthly", description="Trend period: daily, weekly, monthly, yearly"),
    db: Session = Depends(get_postgres_session)
):
    """Get enrollment trends over time"""
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_enrollment_trends(
        department_id=department_id,
        period=period
    )


@router.get("/predictions/student-success")
async def get_student_success_predictions(
    student_id: Optional[int] = Query(None, description="Filter by student ID"),
    course_id: Optional[int] = Query(None, description="Filter by course ID"),
    db: Session = Depends(get_postgres_session)
):
    """Get student success predictions"""
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_student_success_predictions(
        student_id=student_id,
        course_id=course_id
    )


@router.get("/kpis")
async def get_institutional_kpis(
    start_date: Optional[date] = Query(None, description="Start date filter"),
    end_date: Optional[date] = Query(None, description="End date filter"),
    db: Session = Depends(get_postgres_session)
):
    """Get institutional key performance indicators"""
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_institutional_kpis(
        start_date=start_date,
        end_date=end_date
    )
