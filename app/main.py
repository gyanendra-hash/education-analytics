"""
Education Analytics Data Warehouse - Main FastAPI Application
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

from app.core.config import settings
from app.api.api_v1.api import api_router
from app.db.database import init_db
from app.dashboards.dashboard import create_dashboard_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Education Analytics Data Warehouse API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount static files for dashboards
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create and mount dashboard
dashboard_app = create_dashboard_app()
app.mount("/dashboard", dashboard_app, name="dashboard")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Education Analytics Data Warehouse API",
        "version": "1.0.0",
        "docs": "/docs",
        "dashboard": "/dashboard",
        "api": "/api/v1"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "education-analytics"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
