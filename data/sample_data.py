"""
Sample data generation for the Education Analytics Data Warehouse
"""

import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import random
from typing import List, Dict, Any


class SampleDataGenerator:
    """Generate sample data for testing and demonstration"""
    
    def __init__(self):
        self.departments = [
            {"code": "CS", "name": "Computer Science"},
            {"code": "MATH", "name": "Mathematics"},
            {"code": "PHYS", "name": "Physics"},
            {"code": "CHEM", "name": "Chemistry"},
            {"code": "BIO", "name": "Biology"},
            {"code": "ENG", "name": "Engineering"},
            {"code": "BUS", "name": "Business"},
            {"code": "ART", "name": "Arts"}
        ]
        
        self.course_levels = ["undergraduate", "graduate", "doctorate"]
        self.genders = ["male", "female", "other"]
        self.ethnicities = ["White", "Black", "Hispanic", "Asian", "Other"]
        self.student_statuses = ["active", "graduated", "dropped", "suspended"]
        self.letter_grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F"]
        
    def generate_students(self, count: int = 1000) -> pd.DataFrame:
        """Generate sample student data"""
        np.random.seed(42)
        
        students = []
        for i in range(count):
            student = {
                "student_number": f"STU{10000 + i:05d}",
                "first_name": f"Student{i % 100}",
                "last_name": f"LastName{i % 50}",
                "email": f"student{i}@university.edu",
                "date_of_birth": self._random_date(1990, 2005),
                "gender": random.choice(self.genders),
                "ethnicity": random.choice(self.ethnicities),
                "enrollment_date": self._random_date(2018, 2024),
                "graduation_date": self._random_date(2020, 2024) if random.random() > 0.3 else None,
                "status": random.choices(
                    self.student_statuses, 
                    weights=[0.6, 0.25, 0.1, 0.05]
                )[0],
                "major": random.choice([dept["name"] for dept in self.departments]),
                "minor": random.choice([dept["name"] for dept in self.departments]) if random.random() > 0.7 else None,
                "gpa": round(np.random.normal(3.2, 0.5), 2),
                "credits_completed": random.randint(0, 120)
            }
            students.append(student)
        
        return pd.DataFrame(students)
    
    def generate_courses(self, count: int = 200) -> pd.DataFrame:
        """Generate sample course data"""
        np.random.seed(42)
        
        courses = []
        course_codes = set()
        
        for i in range(count):
            dept = random.choice(self.departments)
            level = random.choice(self.course_levels)
            
            # Generate unique course code
            course_code = f"{dept['code']}{random.randint(100, 999)}"
            while course_code in course_codes:
                course_code = f"{dept['code']}{random.randint(100, 999)}"
            course_codes.add(course_code)
            
            course = {
                "course_code": course_code,
                "course_name": f"{dept['name']} {random.randint(100, 999)}",
                "course_description": f"Advanced course in {dept['name'].lower()}",
                "credits": random.choice([1, 2, 3, 4, 6]),
                "level": level,
                "department_id": self.departments.index(dept) + 1,
                "prerequisites": self._generate_prerequisites(),
                "is_active": random.random() > 0.1
            }
            courses.append(course)
        
        return pd.DataFrame(courses)
    
    def generate_instructors(self, count: int = 100) -> pd.DataFrame:
        """Generate sample instructor data"""
        np.random.seed(42)
        
        instructors = []
        for i in range(count):
            instructor = {
                "instructor_number": f"INST{1000 + i:04d}",
                "first_name": f"Instructor{i % 50}",
                "last_name": f"Professor{i % 30}",
                "email": f"instructor{i}@university.edu",
                "title": random.choice([
                    "Professor", "Associate Professor", "Assistant Professor", 
                    "Lecturer", "Adjunct Professor"
                ]),
                "department_id": random.randint(1, len(self.departments)),
                "hire_date": self._random_date(2010, 2023),
                "is_active": random.random() > 0.05
            }
            instructors.append(instructor)
        
        return pd.DataFrame(instructors)
    
    def generate_departments(self) -> pd.DataFrame:
        """Generate department data"""
        departments = []
        for i, dept in enumerate(self.departments):
            department = {
                "department_id": i + 1,
                "department_code": dept["code"],
                "department_name": dept["name"],
                "school_id": random.randint(1, 3),
                "budget": random.randint(500000, 2000000),
                "is_active": True
            }
            departments.append(department)
        
        return pd.DataFrame(departments)
    
    def generate_time_dimension(self, start_year: int = 2018, end_year: int = 2024) -> pd.DataFrame:
        """Generate time dimension data"""
        time_data = []
        current_date = date(start_year, 1, 1)
        end_date = date(end_year, 12, 31)
        
        while current_date <= end_date:
            time_entry = {
                "date": current_date,
                "year": current_date.year,
                "quarter": (current_date.month - 1) // 3 + 1,
                "month": current_date.month,
                "month_name": current_date.strftime("%B"),
                "day": current_date.day,
                "day_of_week": current_date.weekday() + 1,
                "day_name": current_date.strftime("%A"),
                "is_weekend": current_date.weekday() >= 5,
                "is_holiday": self._is_holiday(current_date),
                "semester": self._get_semester(current_date),
                "academic_year": self._get_academic_year(current_date)
            }
            time_data.append(time_entry)
            current_date += timedelta(days=1)
        
        return pd.DataFrame(time_data)
    
    def generate_performance_facts(self, student_count: int = 1000, course_count: int = 200) -> pd.DataFrame:
        """Generate student performance fact data"""
        np.random.seed(42)
        
        performance_data = []
        fact_id = 1
        
        # Generate performance records for each student
        for student_id in range(1, student_count + 1):
            # Each student takes 5-15 courses
            num_courses = random.randint(5, 15)
            courses_taken = random.sample(range(1, course_count + 1), num_courses)
            
            for course_id in courses_taken:
                # Generate performance data
                grade_points = round(np.random.normal(3.0, 0.8), 2)
                grade_points = max(0.0, min(4.0, grade_points))  # Clamp to 0-4 range
                
                letter_grade = self._grade_points_to_letter(grade_points)
                credits_earned = random.choice([1, 2, 3, 4, 6])
                attendance_percentage = round(np.random.normal(85, 10), 1)
                attendance_percentage = max(0, min(100, attendance_percentage))
                
                assignment_score = round(np.random.normal(80, 15), 1)
                assignment_score = max(0, min(100, assignment_score))
                
                exam_score = round(np.random.normal(75, 20), 1)
                exam_score = max(0, min(100, exam_score))
                
                final_score = round((assignment_score * 0.4 + exam_score * 0.6), 1)
                is_pass = final_score >= 60
                
                # Random time within the last 3 years
                random_date = self._random_date(2021, 2024)
                time_id = self._date_to_time_id(random_date)
                
                performance = {
                    "fact_id": fact_id,
                    "student_id": student_id,
                    "course_id": course_id,
                    "instructor_id": random.randint(1, 100),
                    "time_id": time_id,
                    "grade_points": grade_points,
                    "letter_grade": letter_grade,
                    "credits_earned": credits_earned,
                    "attendance_percentage": attendance_percentage,
                    "assignment_score": assignment_score,
                    "exam_score": exam_score,
                    "final_score": final_score,
                    "is_pass": is_pass
                }
                performance_data.append(performance)
                fact_id += 1
        
        return pd.DataFrame(performance_data)
    
    def generate_enrollment_facts(self, student_count: int = 1000, course_count: int = 200) -> pd.DataFrame:
        """Generate enrollment fact data"""
        np.random.seed(42)
        
        enrollment_data = []
        fact_id = 1
        
        for student_id in range(1, student_count + 1):
            # Each student enrolls in 8-20 courses
            num_enrollments = random.randint(8, 20)
            courses_enrolled = random.sample(range(1, course_count + 1), num_enrollments)
            
            for course_id in courses_enrolled:
                enrollment_date = self._random_date(2018, 2024)
                time_id = self._date_to_time_id(enrollment_date)
                
                is_dropped = random.random() < 0.15  # 15% drop rate
                drop_date = None
                if is_dropped:
                    drop_date = enrollment_date + timedelta(days=random.randint(1, 90))
                
                is_completed = not is_dropped and random.random() > 0.1  # 90% completion rate
                waitlist_position = random.randint(1, 10) if random.random() < 0.1 else None
                
                enrollment = {
                    "fact_id": fact_id,
                    "student_id": student_id,
                    "course_id": course_id,
                    "time_id": time_id,
                    "enrollment_date": enrollment_date,
                    "drop_date": drop_date,
                    "is_dropped": is_dropped,
                    "is_completed": is_completed,
                    "waitlist_position": waitlist_position
                }
                enrollment_data.append(enrollment)
                fact_id += 1
        
        return pd.DataFrame(enrollment_data)
    
    def generate_feedback_data(self, count: int = 5000) -> List[Dict[str, Any]]:
        """Generate sample feedback data for MongoDB"""
        np.random.seed(42)
        
        feedback_data = []
        feedback_types = ["course", "instructor", "general", "facility", "support"]
        sentiments = ["positive", "negative", "neutral"]
        tags = ["excellent", "good", "average", "poor", "difficult", "easy", "helpful", "confusing"]
        
        for i in range(count):
            feedback = {
                "student_id": random.randint(1, 1000),
                "course_id": random.randint(1, 200),
                "feedback_type": random.choice(feedback_types),
                "rating": random.randint(1, 5),
                "comment": f"Sample feedback comment {i}",
                "sentiment": random.choice(sentiments),
                "tags": random.sample(tags, random.randint(1, 3)),
                "created_at": self._random_datetime(2023, 2024),
                "updated_at": self._random_datetime(2023, 2024)
            }
            feedback_data.append(feedback)
        
        return feedback_data
    
    def _random_date(self, start_year: int, end_year: int) -> date:
        """Generate random date between start and end year"""
        start_date = date(start_year, 1, 1)
        end_date = date(end_year, 12, 31)
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randint(0, days_between)
        return start_date + timedelta(days=random_days)
    
    def _random_datetime(self, start_year: int, end_year: int) -> datetime:
        """Generate random datetime between start and end year"""
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)
        time_between = end_date - start_date
        seconds_between = time_between.total_seconds()
        random_seconds = random.randint(0, int(seconds_between))
        return start_date + timedelta(seconds=random_seconds)
    
    def _is_holiday(self, date_obj: date) -> bool:
        """Check if date is a holiday (simplified)"""
        # Simplified holiday check - just major holidays
        holidays = [
            (1, 1),   # New Year's Day
            (7, 4),   # Independence Day
            (12, 25), # Christmas
        ]
        return (date_obj.month, date_obj.day) in holidays
    
    def _get_semester(self, date_obj: date) -> str:
        """Get semester based on date"""
        month = date_obj.month
        if month in [1, 2, 3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Fall"
    
    def _get_academic_year(self, date_obj: date) -> str:
        """Get academic year based on date"""
        year = date_obj.year
        month = date_obj.month
        if month >= 8:  # Fall semester starts in August
            return f"{year}-{year + 1}"
        else:
            return f"{year - 1}-{year}"
    
    def _generate_prerequisites(self) -> str:
        """Generate course prerequisites"""
        if random.random() < 0.3:  # 30% of courses have prerequisites
            prereq_courses = random.sample(["CS101", "MATH201", "PHYS301", "CHEM401"], random.randint(1, 2))
            return ", ".join(prereq_courses)
        return None
    
    def _grade_points_to_letter(self, grade_points: float) -> str:
        """Convert grade points to letter grade"""
        if grade_points >= 3.7:
            return "A"
        elif grade_points >= 3.3:
            return "A-"
        elif grade_points >= 3.0:
            return "B+"
        elif grade_points >= 2.7:
            return "B"
        elif grade_points >= 2.3:
            return "B-"
        elif grade_points >= 2.0:
            return "C+"
        elif grade_points >= 1.7:
            return "C"
        elif grade_points >= 1.3:
            return "C-"
        elif grade_points >= 1.0:
            return "D"
        else:
            return "F"
    
    def _date_to_time_id(self, date_obj: date) -> int:
        """Convert date to time_id (simplified)"""
        # This is a simplified mapping - in reality, you'd look up the actual time_id
        days_since_epoch = (date_obj - date(2018, 1, 1)).days
        return days_since_epoch + 1


def generate_all_sample_data():
    """Generate all sample data files"""
    generator = SampleDataGenerator()
    
    print("Generating sample data...")
    
    # Generate dimension tables
    print("Generating students...")
    students_df = generator.generate_students(1000)
    students_df.to_csv("data/students.csv", index=False)
    
    print("Generating courses...")
    courses_df = generator.generate_courses(200)
    courses_df.to_csv("data/courses.csv", index=False)
    
    print("Generating instructors...")
    instructors_df = generator.generate_instructors(100)
    instructors_df.to_csv("data/instructors.csv", index=False)
    
    print("Generating departments...")
    departments_df = generator.generate_departments()
    departments_df.to_csv("data/departments.csv", index=False)
    
    print("Generating time dimension...")
    time_df = generator.generate_time_dimension()
    time_df.to_csv("data/time_dimension.csv", index=False)
    
    # Generate fact tables
    print("Generating performance facts...")
    performance_df = generator.generate_performance_facts(1000, 200)
    performance_df.to_csv("data/performance_facts.csv", index=False)
    
    print("Generating enrollment facts...")
    enrollment_df = generator.generate_enrollment_facts(1000, 200)
    enrollment_df.to_csv("data/enrollment_facts.csv", index=False)
    
    # Generate MongoDB data
    print("Generating feedback data...")
    feedback_data = generator.generate_feedback_data(5000)
    import json
    with open("data/feedback_data.json", "w") as f:
        json.dump(feedback_data, f, indent=2, default=str)
    
    print("Sample data generation completed!")
    print(f"Generated {len(students_df)} students")
    print(f"Generated {len(courses_df)} courses")
    print(f"Generated {len(instructors_df)} instructors")
    print(f"Generated {len(departments_df)} departments")
    print(f"Generated {len(time_df)} time records")
    print(f"Generated {len(performance_df)} performance records")
    print(f"Generated {len(enrollment_df)} enrollment records")
    print(f"Generated {len(feedback_data)} feedback records")


if __name__ == "__main__":
    generate_all_sample_data()
