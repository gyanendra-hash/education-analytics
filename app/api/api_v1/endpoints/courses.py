"""
Course management API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_postgres_session
from app.models.schemas import Course, CourseCreate, CourseUpdate, PaginatedResponse
from app.services.course_service import CourseService

router = APIRouter()


@router.get("/", response_model=PaginatedResponse)
async def get_courses(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    search: Optional[str] = Query(None, description="Search term"),
    level: Optional[str] = Query(None, description="Filter by course level"),
    department_id: Optional[int] = Query(None, description="Filter by department"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_postgres_session)
):
    """Get paginated list of courses with optional filtering"""
    course_service = CourseService(db)
    return await course_service.get_courses_paginated(
        page=page, size=size, search=search, level=level, 
        department_id=department_id, is_active=is_active
    )


@router.get("/{course_id}", response_model=Course)
async def get_course(
    course_id: int,
    db: Session = Depends(get_postgres_session)
):
    """Get course by ID"""
    course_service = CourseService(db)
    course = await course_service.get_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.post("/", response_model=Course)
async def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_postgres_session)
):
    """Create a new course"""
    course_service = CourseService(db)
    return await course_service.create_course(course_data)


@router.put("/{course_id}", response_model=Course)
async def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: Session = Depends(get_postgres_session)
):
    """Update course information"""
    course_service = CourseService(db)
    course = await course_service.update_course(course_id, course_data)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.delete("/{course_id}", response_model=dict)
async def delete_course(
    course_id: int,
    db: Session = Depends(get_postgres_session)
):
    """Delete a course (soft delete by changing status)"""
    course_service = CourseService(db)
    success = await course_service.delete_course(course_id)
    if not success:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course deleted successfully"}


@router.get("/{course_id}/enrollments", response_model=List[dict])
async def get_course_enrollments(
    course_id: int,
    db: Session = Depends(get_postgres_session)
):
    """Get course enrollment data"""
    course_service = CourseService(db)
    return await course_service.get_course_enrollments(course_id)


@router.get("/{course_id}/performance", response_model=List[dict])
async def get_course_performance(
    course_id: int,
    db: Session = Depends(get_postgres_session)
):
    """Get course performance data"""
    course_service = CourseService(db)
    return await course_service.get_course_performance(course_id)


@router.get("/{course_id}/prerequisites", response_model=List[Course])
async def get_course_prerequisites(
    course_id: int,
    db: Session = Depends(get_postgres_session)
):
    """Get course prerequisites"""
    course_service = CourseService(db)
    return await course_service.get_course_prerequisites(course_id)
