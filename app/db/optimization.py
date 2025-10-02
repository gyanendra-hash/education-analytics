"""
Database optimization utilities and indexing strategies
"""

from sqlalchemy import text, Index
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import asyncio
from app.db.database import engine
from app.db.models import (
    DimStudent, DimCourse, DimInstructor, DimDepartment, DimTime,
    StudentPerformanceFact, EnrollmentFact, AttendanceFact
)


class DatabaseOptimizer:
    """Database optimization and indexing utilities"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create_optimized_indexes(self) -> Dict[str, str]:
        """Create optimized indexes for better query performance"""
        results = {}
        
        try:
            # Student table indexes
            await self._create_student_indexes()
            results["student_indexes"] = "Created successfully"
            
            # Course table indexes
            await self._create_course_indexes()
            results["course_indexes"] = "Created successfully"
            
            # Performance fact table indexes
            await self._create_performance_indexes()
            results["performance_indexes"] = "Created successfully"
            
            # Enrollment fact table indexes
            await self._create_enrollment_indexes()
            results["enrollment_indexes"] = "Created successfully"
            
            # Time dimension indexes
            await self._create_time_indexes()
            results["time_indexes"] = "Created successfully"
            
            # Composite indexes for common queries
            await self._create_composite_indexes()
            results["composite_indexes"] = "Created successfully"
            
            # Partial indexes for filtered queries
            await self._create_partial_indexes()
            results["partial_indexes"] = "Created successfully"
            
        except Exception as e:
            results["error"] = f"Failed to create indexes: {str(e)}"
        
        return results
    
    async def _create_student_indexes(self):
        """Create indexes for student dimension table"""
        indexes = [
            # Primary key is already indexed
            "CREATE INDEX IF NOT EXISTS idx_student_number ON dim_student(student_number)",
            "CREATE INDEX IF NOT EXISTS idx_student_email ON dim_student(email)",
            "CREATE INDEX IF NOT EXISTS idx_student_status ON dim_student(status)",
            "CREATE INDEX IF NOT EXISTS idx_student_major ON dim_student(major)",
            "CREATE INDEX IF NOT EXISTS idx_student_enrollment_date ON dim_student(enrollment_date)",
            "CREATE INDEX IF NOT EXISTS idx_student_gpa ON dim_student(gpa)",
            # Composite index for common queries
            "CREATE INDEX IF NOT EXISTS idx_student_status_major ON dim_student(status, major)",
            "CREATE INDEX IF NOT EXISTS idx_student_enrollment_status ON dim_student(enrollment_date, status)"
        ]
        
        for index_sql in indexes:
            await self._execute_sql(index_sql)
    
    async def _create_course_indexes(self):
        """Create indexes for course dimension table"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_course_code ON dim_course(course_code)",
            "CREATE INDEX IF NOT EXISTS idx_course_level ON dim_course(level)",
            "CREATE INDEX IF NOT EXISTS idx_course_department ON dim_course(department_id)",
            "CREATE INDEX IF NOT EXISTS idx_course_active ON dim_course(is_active)",
            "CREATE INDEX IF NOT EXISTS idx_course_credits ON dim_course(credits)",
            # Composite indexes
            "CREATE INDEX IF NOT EXISTS idx_course_dept_level ON dim_course(department_id, level)",
            "CREATE INDEX IF NOT EXISTS idx_course_active_dept ON dim_course(is_active, department_id)"
        ]
        
        for index_sql in indexes:
            await self._execute_sql(index_sql)
    
    async def _create_performance_indexes(self):
        """Create indexes for performance fact table"""
        indexes = [
            # Foreign key indexes
            "CREATE INDEX IF NOT EXISTS idx_perf_student ON student_performance_fact(student_id)",
            "CREATE INDEX IF NOT EXISTS idx_perf_course ON student_performance_fact(course_id)",
            "CREATE INDEX IF NOT EXISTS idx_perf_instructor ON student_performance_fact(instructor_id)",
            "CREATE INDEX IF NOT EXISTS idx_perf_time ON student_performance_fact(time_id)",
            
            # Measure indexes
            "CREATE INDEX IF NOT EXISTS idx_perf_grade_points ON student_performance_fact(grade_points)",
            "CREATE INDEX IF NOT EXISTS idx_perf_letter_grade ON student_performance_fact(letter_grade)",
            "CREATE INDEX IF NOT EXISTS idx_perf_is_pass ON student_performance_fact(is_pass)",
            "CREATE INDEX IF NOT EXISTS idx_perf_final_score ON student_performance_fact(final_score)",
            
            # Composite indexes for common analytical queries
            "CREATE INDEX IF NOT EXISTS idx_perf_student_time ON student_performance_fact(student_id, time_id)",
            "CREATE INDEX IF NOT EXISTS idx_perf_course_time ON student_performance_fact(course_id, time_id)",
            "CREATE INDEX IF NOT EXISTS idx_perf_instructor_time ON student_performance_fact(instructor_id, time_id)",
            "CREATE INDEX IF NOT EXISTS idx_perf_student_course ON student_performance_fact(student_id, course_id)",
            "CREATE INDEX IF NOT EXISTS idx_perf_course_pass ON student_performance_fact(course_id, is_pass)",
            "CREATE INDEX IF NOT EXISTS idx_perf_student_pass ON student_performance_fact(student_id, is_pass)"
        ]
        
        for index_sql in indexes:
            await self._execute_sql(index_sql)
    
    async def _create_enrollment_indexes(self):
        """Create indexes for enrollment fact table"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_enroll_student ON enrollment_fact(student_id)",
            "CREATE INDEX IF NOT EXISTS idx_enroll_course ON enrollment_fact(course_id)",
            "CREATE INDEX IF NOT EXISTS idx_enroll_time ON enrollment_fact(time_id)",
            "CREATE INDEX IF NOT EXISTS idx_enroll_date ON enrollment_fact(enrollment_date)",
            "CREATE INDEX IF NOT EXISTS idx_enroll_dropped ON enrollment_fact(is_dropped)",
            "CREATE INDEX IF NOT EXISTS idx_enroll_completed ON enrollment_fact(is_completed)",
            
            # Composite indexes
            "CREATE INDEX IF NOT EXISTS idx_enroll_student_time ON enrollment_fact(student_id, time_id)",
            "CREATE INDEX IF NOT EXISTS idx_enroll_course_time ON enrollment_fact(course_id, time_id)",
            "CREATE INDEX IF NOT EXISTS idx_enroll_student_course ON enrollment_fact(student_id, course_id)",
            "CREATE INDEX IF NOT EXISTS idx_enroll_course_dropped ON enrollment_fact(course_id, is_dropped)"
        ]
        
        for index_sql in indexes:
            await self._execute_sql(index_sql)
    
    async def _create_time_indexes(self):
        """Create indexes for time dimension table"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_time_date ON dim_time(date)",
            "CREATE INDEX IF NOT EXISTS idx_time_year ON dim_time(year)",
            "CREATE INDEX IF NOT EXISTS idx_time_month ON dim_time(month)",
            "CREATE INDEX IF NOT EXISTS idx_time_quarter ON dim_time(quarter)",
            "CREATE INDEX IF NOT EXISTS idx_time_semester ON dim_time(semester)",
            "CREATE INDEX IF NOT EXISTS idx_time_academic_year ON dim_time(academic_year)",
            
            # Composite indexes
            "CREATE INDEX IF NOT EXISTS idx_time_year_month ON dim_time(year, month)",
            "CREATE INDEX IF NOT EXISTS idx_time_year_quarter ON dim_time(year, quarter)",
            "CREATE INDEX IF NOT EXISTS idx_time_semester_year ON dim_time(semester, academic_year)"
        ]
        
        for index_sql in indexes:
            await self._execute_sql(index_sql)
    
    async def _create_composite_indexes(self):
        """Create composite indexes for complex analytical queries"""
        indexes = [
            # Performance analysis queries
            "CREATE INDEX IF NOT EXISTS idx_perf_analysis ON student_performance_fact(student_id, course_id, time_id, is_pass)",
            "CREATE INDEX IF NOT EXISTS idx_perf_grades ON student_performance_fact(course_id, grade_points, letter_grade)",
            
            # Enrollment analysis queries
            "CREATE INDEX IF NOT EXISTS idx_enroll_analysis ON enrollment_fact(student_id, course_id, time_id, is_dropped, is_completed)",
            
            # Time-based analysis
            "CREATE INDEX IF NOT EXISTS idx_time_analysis ON dim_time(year, quarter, month, semester)",
            
            # Student analysis
            "CREATE INDEX IF NOT EXISTS idx_student_analysis ON dim_student(status, major, enrollment_date, gpa)"
        ]
        
        for index_sql in indexes:
            await self._execute_sql(index_sql)
    
    async def _create_partial_indexes(self):
        """Create partial indexes for filtered queries"""
        indexes = [
            # Active students only
            "CREATE INDEX IF NOT EXISTS idx_student_active ON dim_student(student_id) WHERE status = 'active'",
            
            # Active courses only
            "CREATE INDEX IF NOT EXISTS idx_course_active_only ON dim_course(course_id) WHERE is_active = true",
            
            # Passed performance records only
            "CREATE INDEX IF NOT EXISTS idx_perf_passed ON student_performance_fact(student_id, course_id) WHERE is_pass = true",
            
            # Recent enrollments only (last 2 years)
            "CREATE INDEX IF NOT EXISTS idx_enroll_recent ON enrollment_fact(student_id, course_id) WHERE enrollment_date >= CURRENT_DATE - INTERVAL '2 years'"
        ]
        
        for index_sql in indexes:
            await self._execute_sql(index_sql)
    
    async def _execute_sql(self, sql: str):
        """Execute SQL statement"""
        with engine.connect() as conn:
            conn.execute(text(sql))
            conn.commit()
    
    async def analyze_query_performance(self, query: str) -> Dict[str, Any]:
        """Analyze query performance using EXPLAIN ANALYZE"""
        try:
            explain_query = f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {query}"
            
            with engine.connect() as conn:
                result = conn.execute(text(explain_query))
                plan = result.fetchone()[0]
                
                return {
                    "query": query,
                    "execution_time": plan[0]["Execution Time"],
                    "planning_time": plan[0]["Planning Time"],
                    "total_time": plan[0]["Total Cost"],
                    "plan": plan[0]["Plan"]
                }
        except Exception as e:
            return {"error": f"Failed to analyze query: {str(e)}"}
    
    async def get_index_usage_stats(self) -> List[Dict[str, Any]]:
        """Get index usage statistics"""
        query = """
        SELECT 
            schemaname,
            tablename,
            indexname,
            idx_tup_read,
            idx_tup_fetch,
            idx_scan,
            idx_tup_read / NULLIF(idx_scan, 0) as avg_tuples_per_scan
        FROM pg_stat_user_indexes 
        WHERE schemaname = 'public'
        ORDER BY idx_scan DESC;
        """
        
        with engine.connect() as conn:
            result = conn.execute(text(query))
            return [dict(row) for row in result.fetchall()]
    
    async def get_table_stats(self) -> List[Dict[str, Any]]:
        """Get table statistics"""
        query = """
        SELECT 
            schemaname,
            tablename,
            n_tup_ins as inserts,
            n_tup_upd as updates,
            n_tup_del as deletes,
            n_live_tup as live_tuples,
            n_dead_tup as dead_tuples,
            last_vacuum,
            last_autovacuum,
            last_analyze,
            last_autoanalyze
        FROM pg_stat_user_tables 
        WHERE schemaname = 'public'
        ORDER BY n_live_tup DESC;
        """
        
        with engine.connect() as conn:
            result = conn.execute(text(query))
            return [dict(row) for row in result.fetchall()]
    
    async def optimize_queries(self) -> Dict[str, Any]:
        """Run query optimization recommendations"""
        recommendations = []
        
        # Check for missing indexes
        missing_indexes = await self._find_missing_indexes()
        if missing_indexes:
            recommendations.append({
                "type": "missing_indexes",
                "message": "Consider adding indexes for better performance",
                "details": missing_indexes
            })
        
        # Check for unused indexes
        unused_indexes = await self._find_unused_indexes()
        if unused_indexes:
            recommendations.append({
                "type": "unused_indexes",
                "message": "Consider removing unused indexes to save space",
                "details": unused_indexes
            })
        
        # Check for table bloat
        bloated_tables = await self._find_bloated_tables()
        if bloated_tables:
            recommendations.append({
                "type": "table_bloat",
                "message": "Consider running VACUUM on bloated tables",
                "details": bloated_tables
            })
        
        return {
            "recommendations": recommendations,
            "total_recommendations": len(recommendations)
        }
    
    async def _find_missing_indexes(self) -> List[Dict[str, Any]]:
        """Find potentially missing indexes"""
        # This is a simplified version - in production, you'd use pg_stat_statements
        # and analyze slow queries to identify missing indexes
        return []
    
    async def _find_unused_indexes(self) -> List[Dict[str, Any]]:
        """Find unused indexes"""
        query = """
        SELECT 
            schemaname,
            tablename,
            indexname,
            idx_scan,
            pg_size_pretty(pg_relation_size(indexrelid)) as index_size
        FROM pg_stat_user_indexes 
        WHERE schemaname = 'public' 
        AND idx_scan = 0
        ORDER BY pg_relation_size(indexrelid) DESC;
        """
        
        with engine.connect() as conn:
            result = conn.execute(text(query))
            return [dict(row) for row in result.fetchall()]
    
    async def _find_bloated_tables(self) -> List[Dict[str, Any]]:
        """Find tables with high bloat"""
        query = """
        SELECT 
            schemaname,
            tablename,
            n_dead_tup,
            n_live_tup,
            ROUND((n_dead_tup::float / NULLIF(n_live_tup + n_dead_tup, 0)) * 100, 2) as bloat_percentage
        FROM pg_stat_user_tables 
        WHERE schemaname = 'public'
        AND n_dead_tup > 1000
        ORDER BY bloat_percentage DESC;
        """
        
        with engine.connect() as conn:
            result = conn.execute(text(query))
            return [dict(row) for row in result.fetchall()]
    
    async def create_materialized_views(self) -> Dict[str, str]:
        """Create materialized views for common analytical queries"""
        results = {}
        
        try:
            # Student performance summary
            await self._create_student_performance_summary_view()
            results["student_performance_summary"] = "Created successfully"
            
            # Course performance summary
            await self._create_course_performance_summary_view()
            results["course_performance_summary"] = "Created successfully"
            
            # Department statistics view
            await self._create_department_statistics_view()
            results["department_statistics"] = "Created successfully"
            
            # Monthly enrollment trends view
            await self._create_monthly_enrollment_trends_view()
            results["monthly_enrollment_trends"] = "Created successfully"
            
        except Exception as e:
            results["error"] = f"Failed to create materialized views: {str(e)}"
        
        return results
    
    async def _create_student_performance_summary_view(self):
        """Create materialized view for student performance summary"""
        query = """
        CREATE MATERIALIZED VIEW IF NOT EXISTS mv_student_performance_summary AS
        SELECT 
            s.student_id,
            s.student_number,
            s.first_name,
            s.last_name,
            s.major,
            COUNT(pf.fact_id) as total_courses,
            AVG(pf.grade_points) as avg_gpa,
            SUM(pf.credits_earned) as total_credits,
            COUNT(CASE WHEN pf.is_pass = true THEN 1 END) as passed_courses,
            ROUND(COUNT(CASE WHEN pf.is_pass = true THEN 1 END)::float / COUNT(pf.fact_id) * 100, 2) as pass_rate
        FROM dim_student s
        LEFT JOIN student_performance_fact pf ON s.student_id = pf.student_id
        GROUP BY s.student_id, s.student_number, s.first_name, s.last_name, s.major;
        
        CREATE INDEX IF NOT EXISTS idx_mv_student_perf_student_id ON mv_student_performance_summary(student_id);
        CREATE INDEX IF NOT EXISTS idx_mv_student_perf_major ON mv_student_performance_summary(major);
        CREATE INDEX IF NOT EXISTS idx_mv_student_perf_avg_gpa ON mv_student_performance_summary(avg_gpa);
        """
        
        await self._execute_sql(query)
    
    async def _create_course_performance_summary_view(self):
        """Create materialized view for course performance summary"""
        query = """
        CREATE MATERIALIZED VIEW IF NOT EXISTS mv_course_performance_summary AS
        SELECT 
            c.course_id,
            c.course_code,
            c.course_name,
            c.credits,
            c.level,
            COUNT(pf.fact_id) as total_students,
            AVG(pf.grade_points) as avg_grade_points,
            AVG(pf.final_score) as avg_final_score,
            COUNT(CASE WHEN pf.is_pass = true THEN 1 END) as passed_students,
            ROUND(COUNT(CASE WHEN pf.is_pass = true THEN 1 END)::float / COUNT(pf.fact_id) * 100, 2) as pass_rate
        FROM dim_course c
        LEFT JOIN student_performance_fact pf ON c.course_id = pf.course_id
        GROUP BY c.course_id, c.course_code, c.course_name, c.credits, c.level;
        
        CREATE INDEX IF NOT EXISTS idx_mv_course_perf_course_id ON mv_course_performance_summary(course_id);
        CREATE INDEX IF NOT EXISTS idx_mv_course_perf_level ON mv_course_performance_summary(level);
        CREATE INDEX IF NOT EXISTS idx_mv_course_perf_pass_rate ON mv_course_performance_summary(pass_rate);
        """
        
        await self._execute_sql(query)
    
    async def _create_department_statistics_view(self):
        """Create materialized view for department statistics"""
        query = """
        CREATE MATERIALIZED VIEW IF NOT EXISTS mv_department_statistics AS
        SELECT 
            d.department_id,
            d.department_name,
            COUNT(DISTINCT c.course_id) as total_courses,
            COUNT(DISTINCT s.student_id) as total_students,
            AVG(pf.grade_points) as avg_gpa,
            COUNT(CASE WHEN pf.is_pass = true THEN 1 END) as passed_courses,
            ROUND(COUNT(CASE WHEN pf.is_pass = true THEN 1 END)::float / COUNT(pf.fact_id) * 100, 2) as pass_rate
        FROM dim_department d
        LEFT JOIN dim_course c ON d.department_id = c.department_id
        LEFT JOIN dim_student s ON s.major = c.course_name
        LEFT JOIN student_performance_fact pf ON s.student_id = pf.student_id
        GROUP BY d.department_id, d.department_name;
        
        CREATE INDEX IF NOT EXISTS idx_mv_dept_stats_dept_id ON mv_department_statistics(department_id);
        CREATE INDEX IF NOT EXISTS idx_mv_dept_stats_avg_gpa ON mv_department_statistics(avg_gpa);
        """
        
        await self._execute_sql(query)
    
    async def _create_monthly_enrollment_trends_view(self):
        """Create materialized view for monthly enrollment trends"""
        query = """
        CREATE MATERIALIZED VIEW IF NOT EXISTS mv_monthly_enrollment_trends AS
        SELECT 
            t.year,
            t.month,
            t.month_name,
            t.semester,
            COUNT(DISTINCT ef.student_id) as total_enrollments,
            COUNT(DISTINCT ef.course_id) as unique_courses,
            COUNT(CASE WHEN ef.is_dropped = false THEN 1 END) as active_enrollments,
            COUNT(CASE WHEN ef.is_dropped = true THEN 1 END) as dropped_enrollments
        FROM dim_time t
        LEFT JOIN enrollment_fact ef ON t.time_id = ef.time_id
        GROUP BY t.year, t.month, t.month_name, t.semester
        ORDER BY t.year, t.month;
        
        CREATE INDEX IF NOT EXISTS idx_mv_enroll_trends_year_month ON mv_monthly_enrollment_trends(year, month);
        CREATE INDEX IF NOT EXISTS idx_mv_enroll_trends_semester ON mv_monthly_enrollment_trends(semester);
        """
        
        await self._execute_sql(query)
    
    async def refresh_materialized_views(self) -> Dict[str, str]:
        """Refresh all materialized views"""
        views = [
            "mv_student_performance_summary",
            "mv_course_performance_summary", 
            "mv_department_statistics",
            "mv_monthly_enrollment_trends"
        ]
        
        results = {}
        for view in views:
            try:
                await self._execute_sql(f"REFRESH MATERIALIZED VIEW {view};")
                results[view] = "Refreshed successfully"
            except Exception as e:
                results[view] = f"Failed to refresh: {str(e)}"
        
        return results
