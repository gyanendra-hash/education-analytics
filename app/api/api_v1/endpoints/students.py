"""
Student management API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_postgres_session
from app.models.schemas import Student, StudentCreate, StudentUpdate, PaginatedResponse
from app.services.student_service import StudentService

router = APIRouter()


@router.get("/", response_model=PaginatedResponse)
async def get_students(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    search: Optional[str] = Query(None, description="Search term"),
    status: Optional[str] = Query(None, description="Filter by status"),
    major: Optional[str] = Query(None, description="Filter by major"),
    db: Session = Depends(get_postgres_session)
):
    """Get paginated list of students with optional filtering"""
    student_service = StudentService(db)
    return await student_service.get_students_paginated(
        page=page, size=size, search=search, status=status, major=major
    )


@router.get("/{student_id}", response_model=Student)
async def get_student(
    student_id: int,
    db: Session = Depends(get_postgres_session)
):
    """Get student by ID"""
    student_service = StudentService(db)
    student = await student_service.get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/", response_model=Student)
async def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_postgres_session)
):
    """Create a new student"""
    student_service = StudentService(db)
    return await student_service.create_student(student_data)


@router.put("/{student_id}", response_model=Student)
async def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_postgres_session)
):
    """Update student information"""
    student_service = StudentService(db)
    student = await student_service.update_student(student_id, student_data)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.delete("/{student_id}", response_model=dict)
async def delete_student(
    student_id: int,
    db: Session = Depends(get_postgres_session)
):
    """Delete a student (soft delete by changing status)"""
    student_service = StudentService(db)
    success = await student_service.delete_student(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}


@router.get("/{student_id}/performance", response_model=List[dict])
async def get_student_performance(
    student_id: int,
    db: Session = Depends(get_postgres_session)
):
    """Get student performance data"""
    student_service = StudentService(db)
    return await student_service.get_student_performance(student_id)


@router.get("/{student_id}/courses", response_model=List[dict])
async def get_student_courses(
    student_id: int,
    db: Session = Depends(get_postgres_session)
):
    """Get student's enrolled courses"""
    student_service = StudentService(db)
    return await student_service.get_student_courses(student_id)
