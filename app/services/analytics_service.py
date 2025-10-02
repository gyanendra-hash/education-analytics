"""
Analytics service for data analysis and reporting
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta
from app.db.models import (
    DimStudent, DimCourse, DimInstructor, DimDepartment, DimTime,
    StudentPerformanceFact, EnrollmentFact, AttendanceFact
)
from app.models.schemas import (
    PerformanceMetrics, EnrollmentStats, CourseStats, 
    DepartmentStats, DashboardData
)


class AnalyticsService:
    """Service class for analytics and reporting operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_performance_metrics(
        self,
        student_id: Optional[int] = None,
        course_id: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[PerformanceMetrics]:
        """Get student performance metrics"""
        query = self.db.query(
            StudentPerformanceFact.student_id,
            func.avg(StudentPerformanceFact.grade_points).label('gpa'),
            func.sum(StudentPerformanceFact.credits_earned).label('credits_completed'),
            func.count(StudentPerformanceFact.fact_id).label('courses_taken'),
            func.avg(StudentPerformanceFact.final_score).label('average_grade'),
            func.count(StudentPerformanceFact.fact_id).filter(
                StudentPerformanceFact.is_pass == True
            ).label('passed_courses')
        ).join(
            DimTime, StudentPerformanceFact.time_id == DimTime.time_id
        )
        
        # Apply filters
        if student_id:
            query = query.filter(StudentPerformanceFact.student_id == student_id)
        if course_id:
            query = query.filter(StudentPerformanceFact.course_id == course_id)
        if start_date:
            query = query.filter(DimTime.date >= start_date)
        if end_date:
            query = query.filter(DimTime.date <= end_date)
        
        results = query.group_by(StudentPerformanceFact.student_id).all()
        
        return [
            PerformanceMetrics(
                student_id=result.student_id,
                gpa=float(result.gpa or 0),
                credits_completed=result.credits_completed or 0,
                courses_taken=result.courses_taken or 0,
                average_grade=float(result.average_grade or 0),
                pass_rate=(result.passed_courses / result.courses_taken * 100) if result.courses_taken else 0
            )
            for result in results
        ]
    
    async def get_enrollment_stats(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        department_id: Optional[int] = None
    ) -> EnrollmentStats:
        """Get enrollment statistics"""
        # Base query for students
        student_query = self.db.query(DimStudent)
        if department_id:
            student_query = student_query.join(
                DimCourse, DimStudent.major == DimCourse.course_name  # Simplified join
            ).filter(DimCourse.department_id == department_id)
        
        # Get total students
        total_students = student_query.count()
        
        # Get active students
        active_students = student_query.filter(DimStudent.status == "active").count()
        
        # Get graduated students
        graduated_students = student_query.filter(DimStudent.status == "graduated").count()
        
        # Get new enrollments in period
        if start_date and end_date:
            new_enrollments = student_query.filter(
                and_(
                    DimStudent.enrollment_date >= start_date,
                    DimStudent.enrollment_date <= end_date
                )
            ).count()
        else:
            new_enrollments = 0
        
        # Calculate retention rate (simplified)
        retention_rate = (active_students / total_students * 100) if total_students else 0
        
        return EnrollmentStats(
            total_students=total_students,
            active_students=active_students,
            graduated_students=graduated_students,
            new_enrollments=new_enrollments,
            retention_rate=retention_rate
        )
    
    async def get_course_stats(
        self,
        department_id: Optional[int] = None,
        level: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[CourseStats]:
        """Get course statistics"""
        query = self.db.query(
            DimCourse.course_id,
            DimCourse.course_name,
            func.count(EnrollmentFact.fact_id).label('total_enrollments'),
            func.avg(StudentPerformanceFact.final_score).label('average_grade'),
            func.count(StudentPerformanceFact.fact_id).filter(
                StudentPerformanceFact.is_pass == True
            ).label('passed_students'),
            func.count(StudentPerformanceFact.fact_id).label('total_students')
        ).outerjoin(
            EnrollmentFact, DimCourse.course_id == EnrollmentFact.course_id
        ).outerjoin(
            StudentPerformanceFact, DimCourse.course_id == StudentPerformanceFact.course_id
        )
        
        # Apply filters
        if department_id:
            query = query.filter(DimCourse.department_id == department_id)
        if level:
            query = query.filter(DimCourse.level == level)
        
        results = query.group_by(DimCourse.course_id, DimCourse.course_name).all()
        
        return [
            CourseStats(
                course_id=result.course_id,
                course_name=result.course_name,
                total_enrollments=result.total_enrollments or 0,
                average_grade=float(result.average_grade or 0),
                pass_rate=(result.passed_students / result.total_students * 100) if result.total_students else 0,
                completion_rate=100.0  # Simplified - would need more complex logic
            )
            for result in results
        ]
    
    async def get_department_stats(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[DepartmentStats]:
        """Get department statistics"""
        query = self.db.query(
            DimDepartment.department_id,
            DimDepartment.department_name,
            func.count(DimCourse.course_id).label('total_courses'),
            func.count(DimStudent.student_id).label('total_students'),
            func.avg(StudentPerformanceFact.grade_points).label('average_gpa')
        ).outerjoin(
            DimCourse, DimDepartment.department_id == DimCourse.department_id
        ).outerjoin(
            DimStudent, DimStudent.major == DimCourse.course_name  # Simplified join
        ).outerjoin(
            StudentPerformanceFact, DimStudent.student_id == StudentPerformanceFact.student_id
        )
        
        results = query.group_by(
            DimDepartment.department_id, 
            DimDepartment.department_name
        ).all()
        
        return [
            DepartmentStats(
                department_id=result.department_id,
                department_name=result.department_name,
                total_courses=result.total_courses or 0,
                total_students=result.total_students or 0,
                average_gpa=float(result.average_gpa or 0),
                graduation_rate=85.0  # Simplified - would need more complex logic
            )
            for result in results
        ]
    
    async def get_dashboard_data(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        department_id: Optional[int] = None
    ) -> DashboardData:
        """Get comprehensive dashboard data"""
        # Get performance metrics
        performance_metrics = await self.get_performance_metrics(
            start_date=start_date, end_date=end_date
        )
        
        # Get enrollment stats
        enrollment_stats = await self.get_enrollment_stats(
            start_date=start_date, end_date=end_date, department_id=department_id
        )
        
        # Get course stats
        course_stats = await self.get_course_stats(
            department_id=department_id, start_date=start_date, end_date=end_date
        )
        
        # Get department stats
        department_stats = await self.get_department_stats(
            start_date=start_date, end_date=end_date
        )
        
        # Calculate overall performance metrics
        overall_performance = PerformanceMetrics(
            student_id=0,  # Indicates overall metrics
            gpa=sum(p.gpa for p in performance_metrics) / len(performance_metrics) if performance_metrics else 0,
            credits_completed=sum(p.credits_completed for p in performance_metrics),
            courses_taken=sum(p.courses_taken for p in performance_metrics),
            average_grade=sum(p.average_grade for p in performance_metrics) / len(performance_metrics) if performance_metrics else 0,
            pass_rate=sum(p.pass_rate for p in performance_metrics) / len(performance_metrics) if performance_metrics else 0
        )
        
        return DashboardData(
            performance_metrics=overall_performance,
            enrollment_stats=enrollment_stats,
            course_stats=course_stats,
            department_stats=department_stats
        )
    
    async def get_performance_trends(
        self,
        student_id: Optional[int] = None,
        course_id: Optional[int] = None,
        period: str = "monthly"
    ) -> Dict[str, Any]:
        """Get performance trends over time"""
        # This would implement trend analysis
        # For now, return mock data
        return {
            "period": period,
            "trends": [
                {"date": "2024-01", "gpa": 3.2, "enrollments": 150},
                {"date": "2024-02", "gpa": 3.4, "enrollments": 165},
                {"date": "2024-03", "gpa": 3.3, "enrollments": 158}
            ]
        }
    
    async def get_enrollment_trends(
        self,
        department_id: Optional[int] = None,
        period: str = "monthly"
    ) -> Dict[str, Any]:
        """Get enrollment trends over time"""
        # This would implement enrollment trend analysis
        return {
            "period": period,
            "trends": [
                {"date": "2024-01", "enrollments": 1200, "graduations": 85},
                {"date": "2024-02", "enrollments": 1250, "graduations": 92},
                {"date": "2024-03", "enrollments": 1180, "graduations": 78}
            ]
        }
    
    async def get_student_success_predictions(
        self,
        student_id: Optional[int] = None,
        course_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get student success predictions"""
        # This would implement ML-based predictions
        return {
            "predictions": [
                {
                    "student_id": 1,
                    "success_probability": 0.85,
                    "risk_factors": ["low_attendance", "poor_grades"],
                    "recommendations": ["attend_office_hours", "join_study_group"]
                }
            ]
        }
    
    async def get_institutional_kpis(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Get institutional key performance indicators"""
        enrollment_stats = await self.get_enrollment_stats(start_date, end_date)
        
        return {
            "retention_rate": enrollment_stats.retention_rate,
            "graduation_rate": 78.5,  # Would be calculated from actual data
            "average_gpa": 3.2,  # Would be calculated from actual data
            "student_satisfaction": 4.2,  # Would come from feedback data
            "faculty_ratio": 15.2,  # Would be calculated
            "budget_utilization": 87.3  # Would come from financial data
        }
