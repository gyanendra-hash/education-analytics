@echo off
echo ========================================
echo    Education Analytics - GitHub Push
echo ========================================
echo.

echo [1/6] Checking Git status...
git status
echo.

echo [2/6] Adding all files to Git...
git add .
echo.

echo [3/6] Creating commit...
git commit -m "Initial commit: Education Analytics Data Warehouse

- Complete FastAPI application with PostgreSQL and MongoDB
- ETL pipeline for data processing
- Interactive dashboards with Plotly
- Docker containerization
- Comprehensive API endpoints
- Authentication and security features
- Complete documentation and setup guides
- Added .gitignore, LICENSE, and CONTRIBUTING.md"
echo.

echo [4/6] Setting up main branch...
git branch -M main
echo.

echo [5/6] Adding remote origin...
echo Please enter your GitHub username:
set /p GITHUB_USERNAME=
git remote add origin https://github.com/%GITHUB_USERNAME%/education-analytics.git
echo.

echo [6/6] Pushing to GitHub...
git push -u origin main
echo.

echo ========================================
echo    Push completed successfully!
echo ========================================
echo.
echo Your repository is now available at:
echo https://github.com/%GITHUB_USERNAME%/education-analytics
echo.
echo Next steps:
echo 1. Go to your GitHub repository
echo 2. Add repository description and topics
echo 3. Enable Issues and Wiki if needed
echo 4. Set up branch protection rules
echo.
pause
