#!/usr/bin/env python3
"""
Education Analytics Data Warehouse - Main Entry Point
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.main import app

if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    
    print("🚀 Starting Education Analytics Data Warehouse...")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Reload: {reload}")
    print(f"   Log Level: {log_level}")
    print("\n📊 Available endpoints:")
    print(f"   - API Documentation: http://{host}:{port}/docs")
    print(f"   - Interactive Dashboard: http://{host}:{port}/dashboard")
    print(f"   - Health Check: http://{host}:{port}/health")
    print(f"   - API Base: http://{host}:{port}/api/v1")
    print("\n🔧 To initialize the database, run:")
    print("   python scripts/init_database.py")
    print("\n" + "="*60)
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level,
        access_log=True
    )
