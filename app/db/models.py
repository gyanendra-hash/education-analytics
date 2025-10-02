"""
SQLAlchemy models for the data warehouse
Dimensional modeling with fact and dimension tables
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Boolean, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


# Dimension Tables
class DimStudent(Base):
    """Student dimension table"""
    __tablename__ = "dim_student"
    
    student_id = Column(Integer, primary_key=True, index=True)
    student_number = Column(String(20), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    ethnicity = Column(String(50))
    enrollment_date = Column(Date, nullable=False)
    graduation_date = Column(Date)
    status = Column(String(20), nullable=False)  # active, graduated, dropped
    major = Column(String(100))
    minor = Column(String(100))
    gpa = Column(Float)
    credits_completed = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    performance_facts = relationship("StudentPerformanceFact", back_populates="student")
    enrollment_facts = relationship("EnrollmentFact", back_populates="student")


class DimCourse(Base):
    """Course dimension table"""
    __tablename__ = "dim_course"
    
    course_id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String(20), unique=True, nullable=False, index=True)
    course_name = Column(String(200), nullable=False)
    course_description = Column(Text)
    credits = Column(Integer, nullable=False)
    level = Column(String(20), nullable=False)  # undergraduate, graduate
    department_id = Column(Integer, ForeignKey("dim_department.department_id"))
    prerequisites = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    department = relationship("DimDepartment", back_populates="courses")
    performance_facts = relationship("StudentPerformanceFact", back_populates="course")
    enrollment_facts = relationship("EnrollmentFact", back_populates="course")


class DimInstructor(Base):
    """Instructor dimension table"""
    __tablename__ = "dim_instructor"
    
    instructor_id = Column(Integer, primary_key=True, index=True)
    instructor_number = Column(String(20), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    title = Column(String(50))  # Professor, Associate Professor, etc.
    department_id = Column(Integer, ForeignKey("dim_department.department_id"))
    hire_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    department = relationship("DimDepartment", back_populates="instructors")
    performance_facts = relationship("StudentPerformanceFact", back_populates="instructor")


class DimDepartment(Base):
    """Department dimension table"""
    __tablename__ = "dim_department"
    
    department_id = Column(Integer, primary_key=True, index=True)
    department_code = Column(String(10), unique=True, nullable=False, index=True)
    department_name = Column(String(200), nullable=False)
    school_id = Column(Integer, ForeignKey("dim_school.school_id"))
    budget = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    school = relationship("DimSchool", back_populates="departments")
    courses = relationship("DimCourse", back_populates="department")
    instructors = relationship("DimInstructor", back_populates="department")


class DimSchool(Base):
    """School dimension table"""
    __tablename__ = "dim_school"
    
    school_id = Column(Integer, primary_key=True, index=True)
    school_code = Column(String(10), unique=True, nullable=False, index=True)
    school_name = Column(String(200), nullable=False)
    dean_name = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    departments = relationship("DimDepartment", back_populates="school")


class DimTime(Base):
    """Time dimension table for temporal analysis"""
    __tablename__ = "dim_time"
    
    time_id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    quarter = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False, index=True)
    month_name = Column(String(20), nullable=False)
    day = Column(Integer, nullable=False)
    day_of_week = Column(Integer, nullable=False)
    day_name = Column(String(20), nullable=False)
    is_weekend = Column(Boolean, nullable=False)
    is_holiday = Column(Boolean, default=False)
    semester = Column(String(20))  # Fall, Spring, Summer
    academic_year = Column(String(20))  # 2023-2024
    
    # Relationships
    performance_facts = relationship("StudentPerformanceFact", back_populates="time")
    enrollment_facts = relationship("EnrollmentFact", back_populates="time")


# Fact Tables
class StudentPerformanceFact(Base):
    """Student performance fact table"""
    __tablename__ = "student_performance_fact"
    
    fact_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("dim_student.student_id"), nullable=False)
    course_id = Column(Integer, ForeignKey("dim_course.course_id"), nullable=False)
    instructor_id = Column(Integer, ForeignKey("dim_instructor.instructor_id"), nullable=False)
    time_id = Column(Integer, ForeignKey("dim_time.time_id"), nullable=False)
    
    # Measures
    grade_points = Column(Float, nullable=False)
    letter_grade = Column(String(2), nullable=False)
    credits_earned = Column(Integer, nullable=False)
    attendance_percentage = Column(Float)
    assignment_score = Column(Float)
    exam_score = Column(Float)
    final_score = Column(Float)
    is_pass = Column(Boolean, nullable=False)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    student = relationship("DimStudent", back_populates="performance_facts")
    course = relationship("DimCourse", back_populates="performance_facts")
    instructor = relationship("DimInstructor", back_populates="performance_facts")
    time = relationship("DimTime", back_populates="performance_facts")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_performance_student_time', 'student_id', 'time_id'),
        Index('idx_performance_course_time', 'course_id', 'time_id'),
        Index('idx_performance_instructor_time', 'instructor_id', 'time_id'),
    )


class EnrollmentFact(Base):
    """Enrollment fact table"""
    __tablename__ = "enrollment_fact"
    
    fact_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("dim_student.student_id"), nullable=False)
    course_id = Column(Integer, ForeignKey("dim_course.course_id"), nullable=False)
    time_id = Column(Integer, ForeignKey("dim_time.time_id"), nullable=False)
    
    # Measures
    enrollment_date = Column(Date, nullable=False)
    drop_date = Column(Date)
    is_dropped = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    waitlist_position = Column(Integer)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    student = relationship("DimStudent", back_populates="enrollment_facts")
    course = relationship("DimCourse", back_populates="enrollment_facts")
    time = relationship("DimTime", back_populates="enrollment_facts")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_enrollment_student_time', 'student_id', 'time_id'),
        Index('idx_enrollment_course_time', 'course_id', 'time_id'),
    )


class AttendanceFact(Base):
    """Attendance fact table"""
    __tablename__ = "attendance_fact"
    
    fact_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("dim_student.student_id"), nullable=False)
    course_id = Column(Integer, ForeignKey("dim_course.course_id"), nullable=False)
    time_id = Column(Integer, ForeignKey("dim_time.time_id"), nullable=False)
    
    # Measures
    class_date = Column(Date, nullable=False)
    is_present = Column(Boolean, nullable=False)
    is_late = Column(Boolean, default=False)
    minutes_late = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_attendance_student_date', 'student_id', 'class_date'),
        Index('idx_attendance_course_date', 'course_id', 'class_date'),
    )
