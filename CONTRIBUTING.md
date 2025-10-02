# 🤝 Contributing to Education Analytics

Thank you for your interest in contributing to the Education Analytics Data Warehouse! We welcome contributions from the community and appreciate your help in making this project better.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Issue Guidelines](#issue-guidelines)
- [Pull Request Guidelines](#pull-request-guidelines)

## 📜 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Git
- Docker & Docker Compose (recommended)
- PostgreSQL 13+
- MongoDB 5.0+

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/education_analytics.git
   cd education_analytics
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/originalowner/education_analytics.git
   ```

## 🛠️ Development Setup

### Option 1: Docker Setup (Recommended)

```bash
# Start all services
docker-compose up -d

# Run migrations
docker-compose exec app alembic upgrade head

# Access the application
# API: http://localhost:8000/docs
# Dashboard: http://localhost:8000/dashboard
```

### Option 2: Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Start databases
docker-compose up -d postgres mongodb redis

# Run migrations
alembic upgrade head

# Start the application
uvicorn app.main:app --reload
```

## 🔧 Making Changes

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. Code Quality Standards

We maintain high code quality standards. Please ensure your code follows these guidelines:

#### Python Style
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions small and focused

#### Code Formatting
```bash
# Format code with Black
black app/ tests/

# Sort imports with isort
isort app/ tests/

# Lint with flake8
flake8 app/ tests/
```

#### Testing
- Write tests for new functionality
- Ensure all tests pass
- Aim for good test coverage
- Use descriptive test names

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### 3. Database Changes

If you're making database changes:

```bash
# Create migration
alembic revision --autogenerate -m "Description of changes"

# Apply migration
alembic upgrade head

# Test migration rollback
alembic downgrade -1
alembic upgrade head
```

### 4. Documentation

- Update README.md if needed
- Add docstrings to new functions
- Update API documentation
- Add comments for complex logic

## 📤 Submitting Changes

### 1. Commit Your Changes

```bash
# Add your changes
git add .

# Commit with descriptive message
git commit -m "feat: add student performance prediction model

- Implemented machine learning model for student success prediction
- Added data preprocessing pipeline
- Created API endpoints for predictions
- Added comprehensive tests
- Updated documentation"
```

**Commit Message Format:**
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

### 2. Push Your Branch

```bash
git push origin feature/your-feature-name
```

### 3. Create Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill out the PR template
5. Request review from maintainers

## 🐛 Issue Guidelines

### Before Creating an Issue

1. Search existing issues to avoid duplicates
2. Check if the issue is already fixed
3. Ensure you're using the latest version

### Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the bug
- **Steps to Reproduce**: Detailed steps to reproduce
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: OS, Python version, dependencies
- **Screenshots**: If applicable
- **Logs**: Relevant error messages or logs

### Feature Requests

When requesting features, please include:

- **Use Case**: Why is this feature needed?
- **Proposed Solution**: How should it work?
- **Alternatives**: Other solutions considered
- **Additional Context**: Any other relevant information

## 🔍 Pull Request Guidelines

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Commit messages are descriptive

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests
2. **Code Review**: Maintainers review the code
3. **Testing**: Manual testing if needed
4. **Approval**: At least one approval required
5. **Merge**: Squash and merge to main branch

## 🏷️ Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- `1.0.0` - Initial release
- `1.1.0` - New features
- `1.1.1` - Bug fixes

### Creating Releases

1. Update version in `app/core/config.py`
2. Update CHANGELOG.md
3. Create release tag
4. Generate release notes
5. Publish to PyPI (if applicable)

## 📞 Getting Help

- **Discord**: [Join our community](https://discord.gg/educationanalytics)
- **Email**: dev@educationanalytics.com
- **Issues**: Use GitHub issues for bugs and features
- **Discussions**: Use GitHub discussions for questions

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation
- Annual contributor appreciation

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Education Analytics! 🎉**
