"""
Student service for business logic
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any
from datetime import date
from app.db.models import DimStudent, StudentPerformanceFact, EnrollmentFact
from app.models.schemas import Student, StudentCreate, StudentUpdate, PaginatedResponse


class StudentService:
    """Service class for student-related operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_students_paginated(
        self, 
        page: int, 
        size: int, 
        search: Optional[str] = None,
        status: Optional[str] = None,
        major: Optional[str] = None
    ) -> PaginatedResponse:
        """Get paginated list of students with filtering"""
        query = self.db.query(DimStudent)
        
        # Apply filters
        if search:
            search_filter = or_(
                DimStudent.first_name.ilike(f"%{search}%"),
                DimStudent.last_name.ilike(f"%{search}%"),
                DimStudent.email.ilike(f"%{search}%"),
                DimStudent.student_number.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if status:
            query = query.filter(DimStudent.status == status)
        
        if major:
            query = query.filter(DimStudent.major.ilike(f"%{major}%"))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * size
        students = query.offset(offset).limit(size).all()
        
        # Convert to Pydantic models
        student_list = [Student.from_orm(student) for student in students]
        
        return PaginatedResponse(
            items=student_list,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )
    
    async def get_student_by_id(self, student_id: int) -> Optional[Student]:
        """Get student by ID"""
        student = self.db.query(DimStudent).filter(DimStudent.student_id == student_id).first()
        return Student.from_orm(student) if student else None
    
    async def create_student(self, student_data: StudentCreate) -> Student:
        """Create a new student"""
        # Check if student number or email already exists
        existing = self.db.query(DimStudent).filter(
            or_(
                DimStudent.student_number == student_data.student_number,
                DimStudent.email == student_data.email
            )
        ).first()
        
        if existing:
            raise ValueError("Student with this number or email already exists")
        
        # Create new student
        student = DimStudent(**student_data.dict())
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        
        return Student.from_orm(student)
    
    async def update_student(self, student_id: int, student_data: StudentUpdate) -> Optional[Student]:
        """Update student information"""
        student = self.db.query(DimStudent).filter(DimStudent.student_id == student_id).first()
        if not student:
            return None
        
        # Update fields
        update_data = student_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(student, field, value)
        
        self.db.commit()
        self.db.refresh(student)
        
        return Student.from_orm(student)
    
    async def delete_student(self, student_id: int) -> bool:
        """Soft delete student by changing status"""
        student = self.db.query(DimStudent).filter(DimStudent.student_id == student_id).first()
        if not student:
            return False
        
        student.status = "dropped"
        self.db.commit()
        return True
    
    async def get_student_performance(self, student_id: int) -> List[Dict[str, Any]]:
        """Get student performance data"""
        performance_data = self.db.query(
            StudentPerformanceFact,
            DimStudent.first_name,
            DimStudent.last_name
        ).join(
            DimStudent, StudentPerformanceFact.student_id == DimStudent.student_id
        ).filter(
            StudentPerformanceFact.student_id == student_id
        ).all()
        
        return [
            {
                "fact_id": perf.fact_id,
                "course_id": perf.course_id,
                "instructor_id": perf.instructor_id,
                "grade_points": perf.grade_points,
                "letter_grade": perf.letter_grade,
                "credits_earned": perf.credits_earned,
                "attendance_percentage": perf.attendance_percentage,
                "final_score": perf.final_score,
                "is_pass": perf.is_pass,
                "created_at": perf.created_at
            }
            for perf, first_name, last_name in performance_data
        ]
    
    async def get_student_courses(self, student_id: int) -> List[Dict[str, Any]]:
        """Get student's enrolled courses"""
        courses = self.db.query(EnrollmentFact).filter(
            EnrollmentFact.student_id == student_id
        ).all()
        
        return [
            {
                "fact_id": course.fact_id,
                "course_id": course.course_id,
                "enrollment_date": course.enrollment_date,
                "drop_date": course.drop_date,
                "is_dropped": course.is_dropped,
                "is_completed": course.is_completed,
                "waitlist_position": course.waitlist_position
            }
            for course in courses
        ]
    
    async def get_student_statistics(self, student_id: int) -> Dict[str, Any]:
        """Get comprehensive student statistics"""
        # Get performance summary
        perf_stats = self.db.query(
            func.count(StudentPerformanceFact.fact_id).label('total_courses'),
            func.avg(StudentPerformanceFact.grade_points).label('avg_grade_points'),
            func.sum(StudentPerformanceFact.credits_earned).label('total_credits'),
            func.count(StudentPerformanceFact.fact_id).filter(
                StudentPerformanceFact.is_pass == True
            ).label('passed_courses')
        ).filter(
            StudentPerformanceFact.student_id == student_id
        ).first()
        
        # Get enrollment summary
        enroll_stats = self.db.query(
            func.count(EnrollmentFact.fact_id).label('total_enrollments'),
            func.count(EnrollmentFact.fact_id).filter(
                EnrollmentFact.is_dropped == True
            ).label('dropped_courses')
        ).filter(
            EnrollmentFact.student_id == student_id
        ).first()
        
        return {
            "total_courses": perf_stats.total_courses or 0,
            "average_grade_points": float(perf_stats.avg_grade_points or 0),
            "total_credits": perf_stats.total_credits or 0,
            "passed_courses": perf_stats.passed_courses or 0,
            "total_enrollments": enroll_stats.total_enrollments or 0,
            "dropped_courses": enroll_stats.dropped_courses or 0,
            "pass_rate": (perf_stats.passed_courses / perf_stats.total_courses * 100) if perf_stats.total_courses else 0
        }
