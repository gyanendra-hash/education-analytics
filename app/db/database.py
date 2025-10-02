"""
Database connection and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import asyncio

from app.core.config import settings

# PostgreSQL setup
engine = create_engine(settings.postgres_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB setup
mongodb_client: AsyncIOMotorClient = None
mongodb_sync_client: MongoClient = None


def get_postgres_session():
    """Get PostgreSQL database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """Initialize database connections"""
    global mongodb_client, mongodb_sync_client
    
    # Initialize MongoDB async client
    mongodb_client = AsyncIOMotorClient(settings.mongodb_url)
    
    # Initialize MongoDB sync client for ETL operations
    mongodb_sync_client = MongoClient(settings.mongodb_url)
    
    # Test connections
    try:
        # Test PostgreSQL connection
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("✅ PostgreSQL connection successful")
        
        # Test MongoDB connection
        await mongodb_client.admin.command('ping')
        print("✅ MongoDB connection successful")
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise


def get_mongodb():
    """Get MongoDB database instance"""
    return mongodb_client[settings.MONGODB_DB]


def get_mongodb_sync():
    """Get MongoDB sync database instance for ETL"""
    return mongodb_sync_client[settings.MONGODB_DB]
