@echo off
echo ========================================
echo    Setup Git and Push to GitHub
echo ========================================
echo.

echo [1/7] Initializing Git repository...
git init
echo.

echo [2/7] Adding remote repository...
git remote add origin https://github.com/gyanendra-hash/education-analytics.git
echo.

echo [3/7] Checking Git status...
git status
echo.

echo [4/7] Adding all files to Git...
git add .
echo.

echo [5/7] Creating initial commit...
git commit -m "Initial commit: Education Analytics Data Warehouse

- Complete FastAPI application with PostgreSQL and MongoDB
- ETL pipeline for data processing
- Interactive dashboards with Plotly
- Docker containerization
- Comprehensive API endpoints
- Authentication and security features
- Complete documentation and setup guides
- Added CONTRIBUTING.md for community guidelines
- Added DEPLOYMENT_CHECKLIST.md for setup instructions
- Added LICENSE file (MIT License)
- Added Docker configuration files
- Added .gitignore for Python projects"
echo.

echo [6/7] Setting main branch...
git branch -M main
echo.

echo [7/7] Pushing to GitHub...
git push -u origin main
echo.

echo ========================================
echo    Repository setup completed!
echo ========================================
echo.
echo Your repository is now available at:
echo https://github.com/gyanendra-hash/education-analytics
echo.
echo Files pushed:
echo - Complete FastAPI application
echo - CONTRIBUTING.md (Community guidelines)
echo - DEPLOYMENT_CHECKLIST.md (Setup guide)
echo - LICENSE (MIT License)
echo - Docker files (Dockerfile, docker-compose.yml)
echo - .gitignore (Python project exclusions)
echo - Complete documentation
echo - Sample data and utility scripts
echo.
echo Next steps:
echo 1. Go to your GitHub repository
echo 2. Add repository topics: education, analytics, fastapi, postgresql, mongodb
echo 3. Enable Issues and Wiki
echo 4. Set up branch protection rules
echo 5. Add a detailed repository description
echo.
pause
