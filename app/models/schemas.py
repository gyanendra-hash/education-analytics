"""
Pydantic schemas for API requests and responses
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


# Enums
class StudentStatus(str, Enum):
    ACTIVE = "active"
    GRADUATED = "graduated"
    DROPPED = "dropped"
    SUSPENDED = "suspended"


class CourseLevel(str, Enum):
    UNDERGRADUATE = "undergraduate"
    GRADUATE = "graduate"
    DOCTORATE = "doctorate"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


# Student Schemas
class StudentBase(BaseModel):
    student_number: str = Field(..., description="Unique student number")
    first_name: str = Field(..., description="Student's first name")
    last_name: str = Field(..., description="Student's last name")
    email: EmailStr = Field(..., description="Student's email address")
    date_of_birth: date = Field(..., description="Student's date of birth")
    gender: Gender = Field(..., description="Student's gender")
    ethnicity: Optional[str] = Field(None, description="Student's ethnicity")
    major: Optional[str] = Field(None, description="Student's major")
    minor: Optional[str] = Field(None, description="Student's minor")


class StudentCreate(StudentBase):
    enrollment_date: date = Field(..., description="Student's enrollment date")
    status: StudentStatus = Field(default=StudentStatus.ACTIVE, description="Student's status")


class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    major: Optional[str] = None
    minor: Optional[str] = None
    status: Optional[StudentStatus] = None
    graduation_date: Optional[date] = None


class Student(StudentBase):
    student_id: int = Field(..., description="Unique student ID")
    enrollment_date: date = Field(..., description="Student's enrollment date")
    graduation_date: Optional[date] = Field(None, description="Student's graduation date")
    status: StudentStatus = Field(..., description="Student's status")
    gpa: Optional[float] = Field(None, description="Student's GPA")
    credits_completed: int = Field(default=0, description="Credits completed")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Record update timestamp")
    
    class Config:
        from_attributes = True


# Course Schemas
class CourseBase(BaseModel):
    course_code: str = Field(..., description="Unique course code")
    course_name: str = Field(..., description="Course name")
    course_description: Optional[str] = Field(None, description="Course description")
    credits: int = Field(..., description="Number of credits")
    level: CourseLevel = Field(..., description="Course level")


class CourseCreate(CourseBase):
    department_id: int = Field(..., description="Department ID")
    prerequisites: Optional[str] = Field(None, description="Course prerequisites")


class CourseUpdate(BaseModel):
    course_name: Optional[str] = None
    course_description: Optional[str] = None
    credits: Optional[int] = None
    prerequisites: Optional[str] = None
    is_active: Optional[bool] = None


class Course(CourseBase):
    course_id: int = Field(..., description="Unique course ID")
    department_id: int = Field(..., description="Department ID")
    prerequisites: Optional[str] = Field(None, description="Course prerequisites")
    is_active: bool = Field(default=True, description="Whether course is active")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Record update timestamp")
    
    class Config:
        from_attributes = True


# Performance Schemas
class StudentPerformanceBase(BaseModel):
    student_id: int = Field(..., description="Student ID")
    course_id: int = Field(..., description="Course ID")
    instructor_id: int = Field(..., description="Instructor ID")
    grade_points: float = Field(..., description="Grade points earned")
    letter_grade: str = Field(..., description="Letter grade")
    credits_earned: int = Field(..., description="Credits earned")
    attendance_percentage: Optional[float] = Field(None, description="Attendance percentage")
    assignment_score: Optional[float] = Field(None, description="Assignment score")
    exam_score: Optional[float] = Field(None, description="Exam score")
    final_score: Optional[float] = Field(None, description="Final score")
    is_pass: bool = Field(..., description="Whether student passed")


class StudentPerformanceCreate(StudentPerformanceBase):
    pass


class StudentPerformance(StudentPerformanceBase):
    fact_id: int = Field(..., description="Unique fact ID")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Record update timestamp")
    
    class Config:
        from_attributes = True


# Analytics Schemas
class PerformanceMetrics(BaseModel):
    student_id: int = Field(..., description="Student ID")
    gpa: float = Field(..., description="Current GPA")
    credits_completed: int = Field(..., description="Credits completed")
    courses_taken: int = Field(..., description="Number of courses taken")
    average_grade: float = Field(..., description="Average grade")
    pass_rate: float = Field(..., description="Pass rate percentage")


class EnrollmentStats(BaseModel):
    total_students: int = Field(..., description="Total number of students")
    active_students: int = Field(..., description="Number of active students")
    graduated_students: int = Field(..., description="Number of graduated students")
    new_enrollments: int = Field(..., description="New enrollments this period")
    retention_rate: float = Field(..., description="Student retention rate")


class CourseStats(BaseModel):
    course_id: int = Field(..., description="Course ID")
    course_name: str = Field(..., description="Course name")
    total_enrollments: int = Field(..., description="Total enrollments")
    average_grade: float = Field(..., description="Average grade")
    pass_rate: float = Field(..., description="Pass rate")
    completion_rate: float = Field(..., description="Completion rate")


class DepartmentStats(BaseModel):
    department_id: int = Field(..., description="Department ID")
    department_name: str = Field(..., description="Department name")
    total_courses: int = Field(..., description="Total courses")
    total_students: int = Field(..., description="Total students")
    average_gpa: float = Field(..., description="Average GPA")
    graduation_rate: float = Field(..., description="Graduation rate")


# ETL Schemas
class ETLJobCreate(BaseModel):
    job_type: str = Field(..., description="Type of ETL job")
    file_path: Optional[str] = Field(None, description="Source file path")
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Job parameters")


class ETLJobStatus(BaseModel):
    job_id: str = Field(..., description="ETL job ID")
    status: str = Field(..., description="Job status")
    progress: float = Field(..., description="Job progress percentage")
    records_processed: int = Field(..., description="Records processed")
    records_successful: int = Field(..., description="Records successful")
    records_failed: int = Field(..., description="Records failed")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    start_time: datetime = Field(..., description="Job start time")
    end_time: Optional[datetime] = Field(None, description="Job end time")


# Feedback Schemas
class FeedbackCreate(BaseModel):
    student_id: int = Field(..., description="Student ID")
    course_id: int = Field(..., description="Course ID")
    feedback_type: str = Field(..., description="Type of feedback")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: str = Field(..., description="Feedback comment")
    tags: Optional[List[str]] = Field(default_factory=list, description="Feedback tags")


class Feedback(FeedbackCreate):
    id: str = Field(..., description="Feedback ID")
    sentiment: Optional[str] = Field(None, description="Sentiment analysis result")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Update timestamp")
    
    class Config:
        from_attributes = True


# Dashboard Schemas
class DashboardData(BaseModel):
    performance_metrics: PerformanceMetrics = Field(..., description="Performance metrics")
    enrollment_stats: EnrollmentStats = Field(..., description="Enrollment statistics")
    course_stats: List[CourseStats] = Field(..., description="Course statistics")
    department_stats: List[DepartmentStats] = Field(..., description="Department statistics")


# Response Schemas
class MessageResponse(BaseModel):
    message: str = Field(..., description="Response message")
    success: bool = Field(default=True, description="Success status")


class PaginatedResponse(BaseModel):
    items: List[Any] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")
