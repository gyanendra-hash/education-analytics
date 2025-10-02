"""
Database initialization script
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.core.config import settings
from app.db.database import init_db
from app.db.optimization import DatabaseOptimizer
from app.services.etl_service import ETLService
import pandas as pd
import json


async def initialize_database():
    """Initialize the database with schema and sample data"""
    print("🚀 Initializing Education Analytics Data Warehouse...")
    
    # Initialize database connections
    print("📊 Connecting to databases...")
    await init_db()
    print("✅ Database connections established")
    
    # Create database schema
    print("🏗️ Creating database schema...")
    engine = create_engine(settings.postgres_url)
    
    # Create tables
    from app.db.models import Base
    Base.metadata.create_all(bind=engine)
    print("✅ Database schema created")
    
    # Run database migrations
    print("🔄 Running database migrations...")
    import subprocess
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("✅ Database migrations completed")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Migration warning: {e}")
    
    # Create optimized indexes
    print("⚡ Creating optimized indexes...")
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    optimizer = DatabaseOptimizer(db)
    index_results = await optimizer.create_optimized_indexes()
    print("✅ Indexes created successfully")
    
    # Create materialized views
    print("📈 Creating materialized views...")
    view_results = await optimizer.create_materialized_views()
    print("✅ Materialized views created")
    
    # Load sample data
    print("📝 Loading sample data...")
    await load_sample_data(engine)
    print("✅ Sample data loaded")
    
    # Refresh materialized views
    print("🔄 Refreshing materialized views...")
    refresh_results = await optimizer.refresh_materialized_views()
    print("✅ Materialized views refreshed")
    
    print("🎉 Database initialization completed successfully!")
    
    # Print summary
    print("\n📊 Database Summary:")
    print(f"   - PostgreSQL: {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")
    print(f"   - MongoDB: {settings.MONGODB_HOST}:{settings.MONGODB_PORT}/{settings.MONGODB_DB}")
    print(f"   - Indexes created: {len([k for k in index_results.keys() if 'indexes' in k])}")
    print(f"   - Materialized views: {len([k for k in view_results.keys() if 'summary' in k or 'trends' in k])}")


async def load_sample_data(engine):
    """Load sample data into the database"""
    try:
        # Check if sample data files exist
        data_dir = "data"
        if not os.path.exists(data_dir):
            print("📝 Generating sample data...")
            from data.sample_data import generate_all_sample_data
            generate_all_sample_data()
        
        # Load dimension tables
        await load_dimension_data(engine)
        
        # Load fact tables
        await load_fact_data(engine)
        
        # Load MongoDB data
        await load_mongodb_data()
        
    except Exception as e:
        print(f"⚠️ Warning: Could not load sample data: {e}")
        print("   You can generate sample data later using: python data/sample_data.py")


async def load_dimension_data(engine):
    """Load dimension table data"""
    dimension_files = {
        "departments": "data/departments.csv",
        "time_dimension": "data/time_dimension.csv",
        "students": "data/students.csv",
        "courses": "data/courses.csv",
        "instructors": "data/instructors.csv"
    }
    
    for table_name, file_path in dimension_files.items():
        if os.path.exists(file_path):
            print(f"   Loading {table_name}...")
            df = pd.read_csv(file_path)
            
            # Map table names to actual table names
            table_mapping = {
                "departments": "dim_department",
                "time_dimension": "dim_time",
                "students": "dim_student",
                "courses": "dim_course",
                "instructors": "dim_instructor"
            }
            
            actual_table = table_mapping.get(table_name, table_name)
            df.to_sql(actual_table, engine, if_exists='append', index=False, method='multi')


async def load_fact_data(engine):
    """Load fact table data"""
    fact_files = {
        "performance_facts": "data/performance_facts.csv",
        "enrollment_facts": "data/enrollment_facts.csv"
    }
    
    for table_name, file_path in fact_files.items():
        if os.path.exists(file_path):
            print(f"   Loading {table_name}...")
            df = pd.read_csv(file_path)
            
            # Map table names to actual table names
            table_mapping = {
                "performance_facts": "student_performance_fact",
                "enrollment_facts": "enrollment_fact"
            }
            
            actual_table = table_mapping.get(table_name, table_name)
            df.to_sql(actual_table, engine, if_exists='append', index=False, method='multi')


async def load_mongodb_data():
    """Load MongoDB sample data"""
    try:
        from app.db.database import get_mongodb
        mongodb = get_mongodb()
        
        feedback_file = "data/feedback_data.json"
        if os.path.exists(feedback_file):
            print("   Loading feedback data to MongoDB...")
            with open(feedback_file, 'r') as f:
                feedback_data = json.load(f)
            
            # Insert feedback data
            if feedback_data:
                await mongodb.student_feedback.insert_many(feedback_data)
                print(f"   Inserted {len(feedback_data)} feedback records")
        
    except Exception as e:
        print(f"   Warning: Could not load MongoDB data: {e}")


async def create_sample_schools():
    """Create sample school data"""
    engine = create_engine(settings.postgres_url)
    
    schools_data = [
        {"school_id": 1, "school_code": "ENG", "school_name": "School of Engineering", "dean_name": "Dr. Engineering Dean"},
        {"school_id": 2, "school_code": "SCI", "school_name": "School of Sciences", "dean_name": "Dr. Science Dean"},
        {"school_id": 3, "school_code": "BUS", "school_name": "School of Business", "dean_name": "Dr. Business Dean"}
    ]
    
    schools_df = pd.DataFrame(schools_data)
    schools_df.to_sql("dim_school", engine, if_exists='append', index=False)


if __name__ == "__main__":
    asyncio.run(initialize_database())
