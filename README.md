# FastAPI Task Management API

A RESTful API for managing tasks built with FastAPI, Pydantic, and SQLModel.

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

The API will be available at:
- **API Base URL:** http://localhost:8000
- **Interactive Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## API Endpoints

### Root
- `GET /` - API information and available endpoints

### Health Check
- `GET /health` - API health status

### Task Management
- `POST /tasks` - Create a new task
- `GET /tasks` - List all tasks (with pagination and filtering)
- `GET /tasks/{task_id}` - Get a specific task
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

### Filtering
- `GET /tasks/status/{status}` - Get tasks by status
- `GET /tasks/priority/{priority}` - Get tasks by priority

## Example API Calls

### Create a Task
```bash
curl -X POST "http://localhost:8000/tasks" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "whoami",
       "description": "init0x1",
       "priority": "high",
       "due_date": "2024-01-15T10:00:00"
     }'
```

### Get All Tasks
```bash
curl -X GET "http://localhost:8000/tasks?skip=0&limit=10"
```

### Update a Task
```bash
curl -X PUT "http://localhost:8000/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{
       "status": "in_progress",
       "priority": "urgent"
     }'
```

## Task Status Values
- `pending`
- `in_progress`
- `completed`
- `cancelled`

## Task Priority Values
- `low`
- `medium`
- `high`
- `urgent`

## Project Structure

```
fastapi-task-management/
├── main.py              # FastAPI application entry point
├── models.py            # Pydantic and SQLModel models
├── database.py          # Database configuration
├── crud.py              # Database operations
├── api.py               # API routes
├── requirements.txt     # Python dependencies
└── README.md           
``` 