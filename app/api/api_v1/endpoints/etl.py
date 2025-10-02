"""
ETL (Extract, Transform, Load) API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.db.database import get_postgres_session
from app.models.schemas import ETLJobCreate, ETLJobStatus, MessageResponse
from app.services.etl_service import ETLService

router = APIRouter()


@router.post("/upload", response_model=MessageResponse)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="Data file to upload"),
    file_type: str = "auto",
    db: Session = Depends(get_postgres_session)
):
    """Upload a data file for ETL processing"""
    etl_service = ETLService(db)
    
    # Validate file type
    if not etl_service.validate_file_type(file.filename):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    # Generate job ID
    job_id = str(uuid.uuid4())
    
    # Start ETL job in background
    background_tasks.add_task(
        etl_service.process_file,
        job_id=job_id,
        file=file,
        file_type=file_type
    )
    
    return MessageResponse(
        message=f"File uploaded successfully. Job ID: {job_id}",
        success=True
    )


@router.post("/process", response_model=MessageResponse)
async def start_etl_job(
    background_tasks: BackgroundTasks,
    job_data: ETLJobCreate,
    db: Session = Depends(get_postgres_session)
):
    """Start a new ETL job"""
    etl_service = ETLService(db)
    job_id = str(uuid.uuid4())
    
    # Start ETL job in background
    background_tasks.add_task(
        etl_service.start_etl_job,
        job_id=job_id,
        job_data=job_data
    )
    
    return MessageResponse(
        message=f"ETL job started successfully. Job ID: {job_id}",
        success=True
    )


@router.get("/status/{job_id}", response_model=ETLJobStatus)
async def get_job_status(
    job_id: str,
    db: Session = Depends(get_postgres_session)
):
    """Get ETL job status"""
    etl_service = ETLService(db)
    status = await etl_service.get_job_status(job_id)
    
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return status


@router.get("/jobs", response_model=List[ETLJobStatus])
async def get_all_jobs(
    status: str = None,
    job_type: str = None,
    limit: int = 50,
    db: Session = Depends(get_postgres_session)
):
    """Get all ETL jobs with optional filtering"""
    etl_service = ETLService(db)
    return await etl_service.get_all_jobs(
        status=status,
        job_type=job_type,
        limit=limit
    )


@router.post("/jobs/{job_id}/cancel", response_model=MessageResponse)
async def cancel_job(
    job_id: str,
    db: Session = Depends(get_postgres_session)
):
    """Cancel a running ETL job"""
    etl_service = ETLService(db)
    success = await etl_service.cancel_job(job_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Job not found or cannot be cancelled")
    
    return MessageResponse(
        message="Job cancelled successfully",
        success=True
    )


@router.get("/data-sources")
async def get_data_sources(
    db: Session = Depends(get_postgres_session)
):
    """Get available data sources"""
    etl_service = ETLService(db)
    return await etl_service.get_data_sources()


@router.get("/validation-rules")
async def get_validation_rules(
    data_type: str = None,
    db: Session = Depends(get_postgres_session)
):
    """Get data validation rules"""
    etl_service = ETLService(db)
    return await etl_service.get_validation_rules(data_type)


@router.post("/validate-data")
async def validate_data(
    file: UploadFile = File(..., description="Data file to validate"),
    data_type: str = "auto",
    db: Session = Depends(get_postgres_session)
):
    """Validate data file before processing"""
    etl_service = ETLService(db)
    return await etl_service.validate_data_file(file, data_type)
