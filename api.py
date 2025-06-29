from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from database import get_session
from models import (
    TaskCreate, TaskUpdate, TaskResponse, TaskStatus, TaskPriority,
    APIInfo, HealthResponse
)
from crud import (
    create_task, get_task, get_tasks, get_tasks_by_status, 
    get_tasks_by_priority, update_task, delete_task
)

router = APIRouter()

@router.get("/", response_model=APIInfo, tags=["Root"])
def get_api_info():
    return APIInfo()

@router.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    return HealthResponse()

@router.post("/tasks", response_model=TaskResponse, status_code=201, tags=["Tasks"])
def create_new_task(task: TaskCreate, session: Session = Depends(get_session)):
    try:
        db_task = create_task(session, task)
        return db_task
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tasks", response_model=List[TaskResponse], tags=["Tasks"])
def read_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return"),
    status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by task priority"),
    session: Session = Depends(get_session)
):
    
    tasks = get_tasks(session, skip=skip, limit=limit, status=status, priority=priority)
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def read_task(task_id: int, session: Session = Depends(get_session)):
    """Get a specific task by ID"""
    task = get_task(session, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def update_existing_task(
    task_id: int, 
    task_update: TaskUpdate, 
    session: Session = Depends(get_session)
):
    
    try:
        updated_task = update_task(session, task_id, task_update)
        if updated_task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return updated_task
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/tasks/{task_id}", status_code=204, tags=["Tasks"])
def delete_existing_task(task_id: int, session: Session = Depends(get_session)):
    success = delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

@router.get("/tasks/status/{status}", response_model=List[TaskResponse], tags=["Filtering"])
def read_tasks_by_status(
    status: TaskStatus,
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return"),
    session: Session = Depends(get_session)
):
    tasks = get_tasks_by_status(session, status, skip=skip, limit=limit)
    return tasks

@router.get("/tasks/priority/{priority}", response_model=List[TaskResponse], tags=["Filtering"])
def read_tasks_by_priority(
    priority: TaskPriority,
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return"),
    session: Session = Depends(get_session)
):
    tasks = get_tasks_by_priority(session, priority, skip=skip, limit=limit)
    return tasks 