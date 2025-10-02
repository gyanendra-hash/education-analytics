@echo off
echo ========================================
echo    Update GitHub Repository
echo ========================================
echo.

echo [1/5] Checking Git status...
git status
echo.

echo [2/5] Adding all files to Git...
git add .
echo.

echo [3/5] Creating commit with all essential files...
git commit -m "Add essential open source project files

- Added CONTRIBUTING.md for community guidelines
- Added DEPLOYMENT_CHECKLIST.md for setup instructions
- Added LICENSE file (MIT License)
- Added Docker configuration (Dockerfile, docker-compose.yml)
- Added .gitignore for Python projects
- Added complete FastAPI application structure
- Added ETL pipelines and analytics services
- Added comprehensive documentation
- Added sample data and utility scripts"
echo.

echo [4/5] Checking remote repository...
git remote -v
echo.

echo [5/5] Pushing to GitHub...
git push origin main
echo.

echo ========================================
echo    Repository updated successfully!
echo ========================================
echo.
echo Your updated repository is available at:
echo https://github.com/gyanendra-hash/education-analytics
echo.
echo New files added:
echo - CONTRIBUTING.md (Community guidelines)
echo - DEPLOYMENT_CHECKLIST.md (Setup guide)
echo - LICENSE (MIT License)
echo - Docker files (Dockerfile, docker-compose.yml)
echo - .gitignore (Python project exclusions)
echo - Complete application code
echo - Documentation and samples
echo.
echo Next steps:
echo 1. Go to your GitHub repository
echo 2. Add repository topics: education, analytics, fastapi, postgresql, mongodb
echo 3. Enable Issues and Wiki
echo 4. Set up branch protection rules
echo 5. Add a detailed repository description
echo.
pause
