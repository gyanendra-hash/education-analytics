"""
Main API router that includes all endpoint routers
"""

from fastapi import APIRouter
from app.api.api_v1.endpoints import students, courses, analytics, etl, feedback

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(etl.router, prefix="/etl", tags=["etl"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
