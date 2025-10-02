"""
ETL (Extract, Transform, Load) service for data processing
"""

import pandas as pd
import json
import csv
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import UploadFile
from app.db.database import get_mongodb
from app.db.models import DimStudent, DimCourse, StudentPerformanceFact
from app.models.schemas import ETLJobCreate, ETLJobStatus
from app.core.config import settings


class ETLService:
    """Service class for ETL operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.mongodb = get_mongodb()
        self.jobs_collection = self.mongodb.etl_job_logs
    
    def validate_file_type(self, filename: str) -> bool:
        """Validate uploaded file type"""
        if not filename:
            return False
        
        file_extension = filename.lower().split('.')[-1]
        return f".{file_extension}" in settings.ALLOWED_FILE_TYPES
    
    async def process_file(
        self,
        job_id: str,
        file: UploadFile,
        file_type: str = "auto"
    ) -> None:
        """Process uploaded file through ETL pipeline"""
        try:
            # Log job start
            await self._log_job_start(job_id, "file_upload", file.filename)
            
            # Read file content
            content = await file.read()
            
            # Determine file type
            if file_type == "auto":
                file_type = self._detect_file_type(file.filename)
            
            # Process based on file type
            if file_type == "csv":
                await self._process_csv(job_id, content, file.filename)
            elif file_type == "excel":
                await self._process_excel(job_id, content, file.filename)
            elif file_type == "json":
                await self._process_json(job_id, content, file.filename)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            # Log job completion
            await self._log_job_completion(job_id, True)
            
        except Exception as e:
            # Log job failure
            await self._log_job_completion(job_id, False, str(e))
    
    async def start_etl_job(
        self,
        job_id: str,
        job_data: ETLJobCreate
    ) -> None:
        """Start a new ETL job"""
        try:
            await self._log_job_start(job_id, job_data.job_type, job_data.file_path)
            
            # Process based on job type
            if job_data.job_type == "student_data":
                await self._process_student_data(job_id, job_data.parameters)
            elif job_data.job_type == "course_data":
                await self._process_course_data(job_id, job_data.parameters)
            elif job_data.job_type == "performance_data":
                await self._process_performance_data(job_id, job_data.parameters)
            else:
                raise ValueError(f"Unknown job type: {job_data.job_type}")
            
            await self._log_job_completion(job_id, True)
            
        except Exception as e:
            await self._log_job_completion(job_id, False, str(e))
    
    async def get_job_status(self, job_id: str) -> Optional[ETLJobStatus]:
        """Get ETL job status"""
        job_doc = await self.jobs_collection.find_one({"job_id": job_id})
        if not job_doc:
            return None
        
        return ETLJobStatus(
            job_id=job_doc["job_id"],
            status=job_doc["status"],
            progress=self._calculate_progress(job_doc),
            records_processed=job_doc.get("records_processed", 0),
            records_successful=job_doc.get("records_successful", 0),
            records_failed=job_doc.get("records_failed", 0),
            error_message=job_doc.get("error_message"),
            start_time=job_doc["start_time"],
            end_time=job_doc.get("end_time")
        )
    
    async def get_all_jobs(
        self,
        status: Optional[str] = None,
        job_type: Optional[str] = None,
        limit: int = 50
    ) -> List[ETLJobStatus]:
        """Get all ETL jobs with optional filtering"""
        filter_query = {}
        if status:
            filter_query["status"] = status
        if job_type:
            filter_query["job_type"] = job_type
        
        cursor = self.jobs_collection.find(filter_query).sort("start_time", -1).limit(limit)
        jobs = await cursor.to_list(length=limit)
        
        return [
            ETLJobStatus(
                job_id=job["job_id"],
                status=job["status"],
                progress=self._calculate_progress(job),
                records_processed=job.get("records_processed", 0),
                records_successful=job.get("records_successful", 0),
                records_failed=job.get("records_failed", 0),
                error_message=job.get("error_message"),
                start_time=job["start_time"],
                end_time=job.get("end_time")
            )
            for job in jobs
        ]
    
    async def cancel_job(self, job_id: str) -> bool:
        """Cancel a running ETL job"""
        result = await self.jobs_collection.update_one(
            {"job_id": job_id, "status": "running"},
            {"$set": {"status": "cancelled", "end_time": datetime.utcnow()}}
        )
        return result.modified_count > 0
    
    async def get_data_sources(self) -> List[Dict[str, Any]]:
        """Get available data sources"""
        return [
            {
                "name": "Student Information System",
                "type": "database",
                "description": "Main student database",
                "status": "active"
            },
            {
                "name": "Learning Management System",
                "type": "api",
                "description": "Course and grade data",
                "status": "active"
            },
            {
                "name": "Survey System",
                "type": "file",
                "description": "Student feedback and surveys",
                "status": "active"
            }
        ]
    
    async def get_validation_rules(self, data_type: Optional[str] = None) -> Dict[str, Any]:
        """Get data validation rules"""
        rules = {
            "student": {
                "required_fields": ["student_number", "first_name", "last_name", "email"],
                "email_format": True,
                "date_format": "%Y-%m-%d",
                "gpa_range": [0.0, 4.0]
            },
            "course": {
                "required_fields": ["course_code", "course_name", "credits"],
                "credits_range": [1, 6],
                "level_values": ["undergraduate", "graduate", "doctorate"]
            },
            "performance": {
                "required_fields": ["student_id", "course_id", "grade_points"],
                "grade_range": [0.0, 4.0],
                "letter_grades": ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F"]
            }
        }
        
        if data_type and data_type in rules:
            return rules[data_type]
        return rules
    
    async def validate_data_file(
        self,
        file: UploadFile,
        data_type: str = "auto"
    ) -> Dict[str, Any]:
        """Validate data file before processing"""
        try:
            content = await file.read()
            
            # Detect file type
            if data_type == "auto":
                data_type = self._detect_file_type(file.filename)
            
            # Parse data
            if data_type == "csv":
                df = pd.read_csv(io.StringIO(content.decode('utf-8')))
            elif data_type == "excel":
                df = pd.read_excel(io.BytesIO(content))
            elif data_type == "json":
                data = json.loads(content.decode('utf-8'))
                df = pd.DataFrame(data)
            else:
                raise ValueError(f"Unsupported file type: {data_type}")
            
            # Basic validation
            validation_results = {
                "valid": True,
                "total_records": len(df),
                "errors": [],
                "warnings": []
            }
            
            # Check for empty file
            if len(df) == 0:
                validation_results["valid"] = False
                validation_results["errors"].append("File is empty")
            
            # Check for required columns (basic check)
            required_columns = ["student_number", "first_name", "last_name", "email"]
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                validation_results["warnings"].append(f"Missing columns: {missing_columns}")
            
            return validation_results
            
        except Exception as e:
            return {
                "valid": False,
                "total_records": 0,
                "errors": [str(e)],
                "warnings": []
            }
    
    def _detect_file_type(self, filename: str) -> str:
        """Detect file type from filename"""
        if not filename:
            return "unknown"
        
        extension = filename.lower().split('.')[-1]
        type_mapping = {
            'csv': 'csv',
            'xlsx': 'excel',
            'xls': 'excel',
            'json': 'json',
            'txt': 'csv'
        }
        return type_mapping.get(extension, 'unknown')
    
    async def _process_csv(self, job_id: str, content: bytes, filename: str) -> None:
        """Process CSV file"""
        import io
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        await self._process_dataframe(job_id, df, "csv")
    
    async def _process_excel(self, job_id: str, content: bytes, filename: str) -> None:
        """Process Excel file"""
        import io
        df = pd.read_excel(io.BytesIO(content))
        await self._process_dataframe(job_id, df, "excel")
    
    async def _process_json(self, job_id: str, content: bytes, filename: str) -> None:
        """Process JSON file"""
        data = json.loads(content.decode('utf-8'))
        df = pd.DataFrame(data)
        await self._process_dataframe(job_id, df, "json")
    
    async def _process_dataframe(self, job_id: str, df: pd.DataFrame, file_type: str) -> None:
        """Process pandas DataFrame"""
        records_processed = len(df)
        records_successful = 0
        records_failed = 0
        
        # Update job progress
        await self._update_job_progress(job_id, records_processed, records_successful, records_failed)
        
        # Process each record
        for index, row in df.iterrows():
            try:
                # Transform and load data
                await self._transform_and_load_record(row)
                records_successful += 1
            except Exception as e:
                records_failed += 1
                print(f"Error processing record {index}: {e}")
            
            # Update progress every 100 records
            if (index + 1) % 100 == 0:
                await self._update_job_progress(job_id, records_processed, records_successful, records_failed)
    
    async def _transform_and_load_record(self, row: pd.Series) -> None:
        """Transform and load a single record"""
        # This would contain the actual transformation logic
        # For now, just a placeholder
        pass
    
    async def _process_student_data(self, job_id: str, parameters: Dict[str, Any]) -> None:
        """Process student data ETL job"""
        # Implementation for student data processing
        pass
    
    async def _process_course_data(self, job_id: str, parameters: Dict[str, Any]) -> None:
        """Process course data ETL job"""
        # Implementation for course data processing
        pass
    
    async def _process_performance_data(self, job_id: str, parameters: Dict[str, Any]) -> None:
        """Process performance data ETL job"""
        # Implementation for performance data processing
        pass
    
    async def _log_job_start(self, job_id: str, job_type: str, file_path: Optional[str] = None) -> None:
        """Log ETL job start"""
        job_doc = {
            "job_id": job_id,
            "job_type": job_type,
            "status": "running",
            "start_time": datetime.utcnow(),
            "file_path": file_path,
            "records_processed": 0,
            "records_successful": 0,
            "records_failed": 0
        }
        await self.jobs_collection.insert_one(job_doc)
    
    async def _log_job_completion(self, job_id: str, success: bool, error_message: Optional[str] = None) -> None:
        """Log ETL job completion"""
        update_data = {
            "status": "completed" if success else "failed",
            "end_time": datetime.utcnow()
        }
        
        if error_message:
            update_data["error_message"] = error_message
        
        await self.jobs_collection.update_one(
            {"job_id": job_id},
            {"$set": update_data}
        )
    
    async def _update_job_progress(
        self,
        job_id: str,
        records_processed: int,
        records_successful: int,
        records_failed: int
    ) -> None:
        """Update job progress"""
        await self.jobs_collection.update_one(
            {"job_id": job_id},
            {
                "$set": {
                    "records_processed": records_processed,
                    "records_successful": records_successful,
                    "records_failed": records_failed
                }
            }
        )
    
    def _calculate_progress(self, job_doc: Dict[str, Any]) -> float:
        """Calculate job progress percentage"""
        if job_doc["status"] == "completed":
            return 100.0
        elif job_doc["status"] == "failed":
            return 0.0
        
        total_records = job_doc.get("records_processed", 0)
        if total_records == 0:
            return 0.0
        
        # This is a simplified calculation
        return min(100.0, (total_records / 1000) * 100)
