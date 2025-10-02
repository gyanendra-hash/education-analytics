"""
Course service for business logic
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any
from app.db.models import DimCourse, DimDepartment, StudentPerformanceFact, EnrollmentFact
from app.models.schemas import Course, CourseCreate, CourseUpdate, PaginatedResponse


class CourseService:
    """Service class for course-related operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_courses_paginated(
        self,
        page: int,
        size: int,
        search: Optional[str] = None,
        level: Optional[str] = None,
        department_id: Optional[int] = None,
        is_active: Optional[bool] = None
    ) -> PaginatedResponse:
        """Get paginated list of courses with filtering"""
        query = self.db.query(DimCourse)
        
        # Apply filters
        if search:
            search_filter = or_(
                DimCourse.course_name.ilike(f"%{search}%"),
                DimCourse.course_code.ilike(f"%{search}%"),
                DimCourse.course_description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if level:
            query = query.filter(DimCourse.level == level)
        
        if department_id:
            query = query.filter(DimCourse.department_id == department_id)
        
        if is_active is not None:
            query = query.filter(DimCourse.is_active == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * size
        courses = query.offset(offset).limit(size).all()
        
        # Convert to Pydantic models
        course_list = [Course.from_orm(course) for course in courses]
        
        return PaginatedResponse(
            items=course_list,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )
    
    async def get_course_by_id(self, course_id: int) -> Optional[Course]:
        """Get course by ID"""
        course = self.db.query(DimCourse).filter(DimCourse.course_id == course_id).first()
        return Course.from_orm(course) if course else None
    
    async def create_course(self, course_data: CourseCreate) -> Course:
        """Create a new course"""
        # Check if course code already exists
        existing = self.db.query(DimCourse).filter(
            DimCourse.course_code == course_data.course_code
        ).first()
        
        if existing:
            raise ValueError("Course with this code already exists")
        
        # Create new course
        course = DimCourse(**course_data.dict())
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        
        return Course.from_orm(course)
    
    async def update_course(self, course_id: int, course_data: CourseUpdate) -> Optional[Course]:
        """Update course information"""
        course = self.db.query(DimCourse).filter(DimCourse.course_id == course_id).first()
        if not course:
            return None
        
        # Update fields
        update_data = course_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(course, field, value)
        
        self.db.commit()
        self.db.refresh(course)
        
        return Course.from_orm(course)
    
    async def delete_course(self, course_id: int) -> bool:
        """Soft delete course by changing status"""
        course = self.db.query(DimCourse).filter(DimCourse.course_id == course_id).first()
        if not course:
            return False
        
        course.is_active = False
        self.db.commit()
        return True
    
    async def get_course_enrollments(self, course_id: int) -> List[Dict[str, Any]]:
        """Get course enrollment data"""
        enrollments = self.db.query(EnrollmentFact).filter(
            EnrollmentFact.course_id == course_id
        ).all()
        
        return [
            {
                "fact_id": enrollment.fact_id,
                "student_id": enrollment.student_id,
                "enrollment_date": enrollment.enrollment_date,
                "drop_date": enrollment.drop_date,
                "is_dropped": enrollment.is_dropped,
                "is_completed": enrollment.is_completed,
                "waitlist_position": enrollment.waitlist_position
            }
            for enrollment in enrollments
        ]
    
    async def get_course_performance(self, course_id: int) -> List[Dict[str, Any]]:
        """Get course performance data"""
        performance_data = self.db.query(StudentPerformanceFact).filter(
            StudentPerformanceFact.course_id == course_id
        ).all()
        
        return [
            {
                "fact_id": perf.fact_id,
                "student_id": perf.student_id,
                "instructor_id": perf.instructor_id,
                "grade_points": perf.grade_points,
                "letter_grade": perf.letter_grade,
                "credits_earned": perf.credits_earned,
                "attendance_percentage": perf.attendance_percentage,
                "final_score": perf.final_score,
                "is_pass": perf.is_pass,
                "created_at": perf.created_at
            }
            for perf in performance_data
        ]
    
    async def get_course_prerequisites(self, course_id: int) -> List[Course]:
        """Get course prerequisites"""
        course = self.db.query(DimCourse).filter(DimCourse.course_id == course_id).first()
        if not course or not course.prerequisites:
            return []
        
        # Parse prerequisites (assuming comma-separated course codes)
        prereq_codes = [code.strip() for code in course.prerequisites.split(',')]
        
        # Get prerequisite courses
        prereq_courses = self.db.query(DimCourse).filter(
            DimCourse.course_code.in_(prereq_codes)
        ).all()
        
        return [Course.from_orm(course) for course in prereq_courses]
    
    async def get_course_statistics(self, course_id: int) -> Dict[str, Any]:
        """Get comprehensive course statistics"""
        # Get enrollment statistics
        enroll_stats = self.db.query(
            func.count(EnrollmentFact.fact_id).label('total_enrollments'),
            func.count(EnrollmentFact.fact_id).filter(
                EnrollmentFact.is_dropped == False
            ).label('active_enrollments'),
            func.count(EnrollmentFact.fact_id).filter(
                EnrollmentFact.is_completed == True
            ).label('completed_enrollments')
        ).filter(
            EnrollmentFact.course_id == course_id
        ).first()
        
        # Get performance statistics
        perf_stats = self.db.query(
            func.count(StudentPerformanceFact.fact_id).label('total_grades'),
            func.avg(StudentPerformanceFact.grade_points).label('avg_grade_points'),
            func.avg(StudentPerformanceFact.final_score).label('avg_final_score'),
            func.count(StudentPerformanceFact.fact_id).filter(
                StudentPerformanceFact.is_pass == True
            ).label('passed_students')
        ).filter(
            StudentPerformanceFact.course_id == course_id
        ).first()
        
        return {
            "total_enrollments": enroll_stats.total_enrollments or 0,
            "active_enrollments": enroll_stats.active_enrollments or 0,
            "completed_enrollments": enroll_stats.completed_enrollments or 0,
            "total_grades": perf_stats.total_grades or 0,
            "average_grade_points": float(perf_stats.avg_grade_points or 0),
            "average_final_score": float(perf_stats.avg_final_score or 0),
            "passed_students": perf_stats.passed_students or 0,
            "pass_rate": (perf_stats.passed_students / perf_stats.total_grades * 100) if perf_stats.total_grades else 0
        }
