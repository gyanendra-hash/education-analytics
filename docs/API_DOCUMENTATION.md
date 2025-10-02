# Education Analytics Data Warehouse - API Documentation

## Overview

The Education Analytics Data Warehouse provides a comprehensive REST API for managing and analyzing educational data. The API is built with FastAPI and provides endpoints for student management, course analytics, performance tracking, and institutional reporting.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, the API does not require authentication for demonstration purposes. In production, JWT-based authentication should be implemented.

## API Endpoints

### Students

#### Get All Students
```http
GET /students
```

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `size` (int): Page size (default: 10, max: 100)
- `search` (string): Search term for name, email, or student number
- `status` (string): Filter by student status (active, graduated, dropped, suspended)
- `major` (string): Filter by major

**Response:**
```json
{
  "items": [
    {
      "student_id": 1,
      "student_number": "STU10001",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@university.edu",
      "date_of_birth": "2000-01-15",
      "gender": "male",
      "ethnicity": "White",
      "enrollment_date": "2020-09-01",
      "graduation_date": null,
      "status": "active",
      "major": "Computer Science",
      "minor": "Mathematics",
      "gpa": 3.5,
      "credits_completed": 90,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": null
    }
  ],
  "total": 1000,
  "page": 1,
  "size": 10,
  "pages": 100
}
```

#### Get Student by ID
```http
GET /students/{student_id}
```

**Response:**
```json
{
  "student_id": 1,
  "student_number": "STU10001",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@university.edu",
  "date_of_birth": "2000-01-15",
  "gender": "male",
  "ethnicity": "White",
  "enrollment_date": "2020-09-01",
  "graduation_date": null,
  "status": "active",
  "major": "Computer Science",
  "minor": "Mathematics",
  "gpa": 3.5,
  "credits_completed": 90,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

#### Create Student
```http
POST /students
```

**Request Body:**
```json
{
  "student_number": "STU10002",
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane.smith@university.edu",
  "date_of_birth": "2001-03-20",
  "gender": "female",
  "ethnicity": "Asian",
  "enrollment_date": "2024-09-01",
  "status": "active",
  "major": "Mathematics"
}
```

#### Update Student
```http
PUT /students/{student_id}
```

**Request Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith-Johnson",
  "email": "jane.smith@university.edu",
  "major": "Computer Science",
  "status": "active"
}
```

#### Delete Student
```http
DELETE /students/{student_id}
```

**Response:**
```json
{
  "message": "Student deleted successfully"
}
```

#### Get Student Performance
```http
GET /students/{student_id}/performance
```

**Response:**
```json
[
  {
    "fact_id": 1,
    "course_id": 101,
    "instructor_id": 1,
    "grade_points": 3.5,
    "letter_grade": "A-",
    "credits_earned": 3,
    "attendance_percentage": 95.5,
    "final_score": 88.0,
    "is_pass": true,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### Courses

#### Get All Courses
```http
GET /courses
```

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `size` (int): Page size (default: 10, max: 100)
- `search` (string): Search term for course name or code
- `level` (string): Filter by course level (undergraduate, graduate, doctorate)
- `department_id` (int): Filter by department ID
- `is_active` (boolean): Filter by active status

#### Get Course by ID
```http
GET /courses/{course_id}
```

#### Create Course
```http
POST /courses
```

**Request Body:**
```json
{
  "course_code": "CS401",
  "course_name": "Advanced Algorithms",
  "course_description": "Advanced algorithmic techniques and analysis",
  "credits": 3,
  "level": "undergraduate",
  "department_id": 1,
  "prerequisites": "CS201, MATH301"
}
```

#### Update Course
```http
PUT /courses/{course_id}
```

#### Delete Course
```http
DELETE /courses/{course_id}
```

### Analytics

#### Get Performance Metrics
```http
GET /analytics/performance
```

**Query Parameters:**
- `student_id` (int): Filter by student ID
- `course_id` (int): Filter by course ID
- `start_date` (date): Start date filter (YYYY-MM-DD)
- `end_date` (date): End date filter (YYYY-MM-DD)

**Response:**
```json
[
  {
    "student_id": 1,
    "gpa": 3.5,
    "credits_completed": 90,
    "courses_taken": 15,
    "average_grade": 85.5,
    "pass_rate": 93.3
  }
]
```

#### Get Enrollment Statistics
```http
GET /analytics/enrollment
```

**Query Parameters:**
- `start_date` (date): Start date filter
- `end_date` (date): End date filter
- `department_id` (int): Filter by department

**Response:**
```json
{
  "total_students": 2847,
  "active_students": 2150,
  "graduated_students": 650,
  "new_enrollments": 342,
  "retention_rate": 87.3
}
```

#### Get Course Statistics
```http
GET /analytics/courses
```

**Query Parameters:**
- `department_id` (int): Filter by department
- `level` (string): Filter by course level
- `start_date` (date): Start date filter
- `end_date` (date): End date filter

**Response:**
```json
[
  {
    "course_id": 101,
    "course_name": "Introduction to Computer Science",
    "total_enrollments": 150,
    "average_grade": 82.5,
    "pass_rate": 88.7,
    "completion_rate": 92.0
  }
]
```

#### Get Department Statistics
```http
GET /analytics/departments
```

**Response:**
```json
[
  {
    "department_id": 1,
    "department_name": "Computer Science",
    "total_courses": 45,
    "total_students": 850,
    "average_gpa": 3.4,
    "graduation_rate": 85.2
  }
]
```

#### Get Dashboard Data
```http
GET /analytics/dashboard
```

**Query Parameters:**
- `start_date` (date): Start date filter
- `end_date` (date): End date filter
- `department_id` (int): Filter by department

**Response:**
```json
{
  "performance_metrics": {
    "student_id": 0,
    "gpa": 3.24,
    "credits_completed": 45000,
    "courses_taken": 12000,
    "average_grade": 82.5,
    "pass_rate": 87.3
  },
  "enrollment_stats": {
    "total_students": 2847,
    "active_students": 2150,
    "graduated_students": 650,
    "new_enrollments": 342,
    "retention_rate": 87.3
  },
  "course_stats": [...],
  "department_stats": [...]
}
```

#### Get Performance Trends
```http
GET /analytics/trends/performance
```

**Query Parameters:**
- `student_id` (int): Filter by student ID
- `course_id` (int): Filter by course ID
- `period` (string): Trend period (daily, weekly, monthly, yearly)

#### Get Enrollment Trends
```http
GET /analytics/trends/enrollment
```

**Query Parameters:**
- `department_id` (int): Filter by department
- `period` (string): Trend period (daily, weekly, monthly, yearly)

#### Get Student Success Predictions
```http
GET /analytics/predictions/student-success
```

**Query Parameters:**
- `student_id` (int): Filter by student ID
- `course_id` (int): Filter by course ID

#### Get Institutional KPIs
```http
GET /analytics/kpis
```

**Query Parameters:**
- `start_date` (date): Start date filter
- `end_date` (date): End date filter

### ETL Operations

#### Upload File
```http
POST /etl/upload
```

**Form Data:**
- `file`: Data file (CSV, Excel, JSON)
- `file_type`: File type (auto, csv, excel, json)

**Response:**
```json
{
  "message": "File uploaded successfully. Job ID: 123e4567-e89b-12d3-a456-426614174000",
  "success": true
}
```

#### Start ETL Job
```http
POST /etl/process
```

**Request Body:**
```json
{
  "job_type": "student_data",
  "file_path": "/path/to/file.csv",
  "parameters": {
    "batch_size": 1000,
    "validate_data": true
  }
}
```

#### Get Job Status
```http
GET /etl/status/{job_id}
```

**Response:**
```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "running",
  "progress": 45.5,
  "records_processed": 450,
  "records_successful": 445,
  "records_failed": 5,
  "error_message": null,
  "start_time": "2024-01-01T10:00:00Z",
  "end_time": null
}
```

#### Get All Jobs
```http
GET /etl/jobs
```

**Query Parameters:**
- `status` (string): Filter by job status
- `job_type` (string): Filter by job type
- `limit` (int): Limit number of results (default: 50)

#### Cancel Job
```http
POST /etl/jobs/{job_id}/cancel
```

#### Get Data Sources
```http
GET /etl/data-sources
```

#### Get Validation Rules
```http
GET /etl/validation-rules
```

**Query Parameters:**
- `data_type` (string): Data type (student, course, performance)

#### Validate Data File
```http
POST /etl/validate-data
```

**Form Data:**
- `file`: Data file to validate
- `data_type`: Data type (auto, student, course, performance)

### Feedback

#### Get All Feedback
```http
GET /feedback
```

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `size` (int): Page size (default: 10, max: 100)
- `student_id` (int): Filter by student ID
- `course_id` (int): Filter by course ID
- `feedback_type` (string): Filter by feedback type
- `rating_min` (int): Minimum rating (1-5)
- `rating_max` (int): Maximum rating (1-5)

#### Get Feedback by ID
```http
GET /feedback/{feedback_id}
```

#### Create Feedback
```http
POST /feedback
```

**Request Body:**
```json
{
  "student_id": 1,
  "course_id": 101,
  "feedback_type": "course",
  "rating": 4,
  "comment": "Great course with excellent instructor!",
  "tags": ["excellent", "helpful"]
}
```

#### Get Sentiment Analysis
```http
GET /feedback/analytics/sentiment
```

**Query Parameters:**
- `student_id` (int): Filter by student ID
- `course_id` (int): Filter by course ID
- `feedback_type` (string): Filter by feedback type
- `start_date` (string): Start date filter
- `end_date` (string): End date filter

#### Get Feedback Trends
```http
GET /feedback/analytics/trends
```

**Query Parameters:**
- `student_id` (int): Filter by student ID
- `course_id` (int): Filter by course ID
- `period` (string): Trend period (daily, weekly, monthly)

#### Get Rating Distribution
```http
GET /feedback/analytics/ratings
```

#### Get Popular Tags
```http
GET /feedback/tags/popular
```

**Query Parameters:**
- `limit` (int): Number of tags to return (default: 20)

#### Bulk Import Feedback
```http
POST /feedback/bulk-import
```

**Request Body:**
```json
[
  {
    "student_id": 1,
    "course_id": 101,
    "feedback_type": "course",
    "rating": 4,
    "comment": "Great course!",
    "tags": ["excellent"]
  },
  {
    "student_id": 2,
    "course_id": 102,
    "feedback_type": "instructor",
    "rating": 5,
    "comment": "Amazing instructor!",
    "tags": ["helpful", "knowledgeable"]
  }
]
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "error message",
      "type": "error_type"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse. Current limits:
- 100 requests per minute per IP address
- 1000 requests per hour per IP address

## Pagination

Most list endpoints support pagination with the following parameters:
- `page`: Page number (1-based)
- `size`: Number of items per page (max 100)

Response includes pagination metadata:
- `total`: Total number of items
- `page`: Current page number
- `size`: Page size
- `pages`: Total number of pages

## Filtering and Sorting

Many endpoints support filtering and sorting:
- Use query parameters for filtering
- Use `sort` parameter for sorting (e.g., `sort=name` or `sort=-created_at`)
- Use `search` parameter for text search across multiple fields

## Data Formats

### Dates
All dates are in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)

### File Uploads
Supported file formats:
- CSV (.csv)
- Excel (.xlsx, .xls)
- JSON (.json)

Maximum file size: 10MB

## WebSocket Support

Real-time updates are available via WebSocket connections:
- Endpoint: `ws://localhost:8000/ws`
- Events: `student_updated`, `course_updated`, `performance_updated`

## SDKs and Libraries

Official SDKs are available for:
- Python: `pip install education-analytics-sdk`
- JavaScript: `npm install @education-analytics/sdk`
- R: `install.packages("educationAnalytics")`

## Support

For API support and questions:
- Documentation: https://docs.education-analytics.com
- Support Email: support@education-analytics.com
- GitHub Issues: https://github.com/education-analytics/api/issues
