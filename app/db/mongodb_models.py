"""
MongoDB document models for semi-structured data
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class StudentFeedback(BaseModel):
    """Student feedback document model"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    student_id: int = Field(..., description="Student ID from PostgreSQL")
    course_id: int = Field(..., description="Course ID from PostgreSQL")
    feedback_type: str = Field(..., description="Type of feedback: course, instructor, general")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: str = Field(..., description="Feedback comment")
    sentiment: Optional[str] = Field(None, description="Sentiment analysis result")
    tags: List[str] = Field(default_factory=list, description="Feedback tags")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class SystemLog(BaseModel):
    """System log document model"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    level: str = Field(..., description="Log level: INFO, WARNING, ERROR, DEBUG")
    message: str = Field(..., description="Log message")
    module: str = Field(..., description="Module that generated the log")
    user_id: Optional[int] = Field(None, description="User ID if applicable")
    session_id: Optional[str] = Field(None, description="Session ID")
    ip_address: Optional[str] = Field(None, description="IP address")
    user_agent: Optional[str] = Field(None, description="User agent string")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class SurveyResponse(BaseModel):
    """Survey response document model"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    survey_id: str = Field(..., description="Survey identifier")
    student_id: int = Field(..., description="Student ID from PostgreSQL")
    responses: Dict[str, Any] = Field(..., description="Survey responses")
    completion_percentage: float = Field(..., ge=0, le=100, description="Completion percentage")
    time_spent: int = Field(..., description="Time spent in seconds")
    device_type: Optional[str] = Field(None, description="Device type used")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class PerformanceMetrics(BaseModel):
    """Real-time performance metrics document model"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    metric_name: str = Field(..., description="Name of the metric")
    metric_value: float = Field(..., description="Metric value")
    metric_unit: str = Field(..., description="Unit of measurement")
    category: str = Field(..., description="Metric category: academic, financial, operational")
    student_id: Optional[int] = Field(None, description="Student ID if student-specific")
    course_id: Optional[int] = Field(None, description="Course ID if course-specific")
    department_id: Optional[int] = Field(None, description="Department ID if department-specific")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ETLJobLog(BaseModel):
    """ETL job execution log document model"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    job_id: str = Field(..., description="ETL job identifier")
    job_type: str = Field(..., description="Type of ETL job")
    status: str = Field(..., description="Job status: running, completed, failed")
    start_time: datetime = Field(..., description="Job start time")
    end_time: Optional[datetime] = Field(None, description="Job end time")
    records_processed: int = Field(default=0, description="Number of records processed")
    records_successful: int = Field(default=0, description="Number of successful records")
    records_failed: int = Field(default=0, description="Number of failed records")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    file_path: Optional[str] = Field(None, description="Source file path")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
