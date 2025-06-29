from datetime import datetime, date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, validator
from sqlmodel import SQLModel, Field as SQLField


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"

# SQLModel for database
class Task(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    title: str = SQLField(max_length=200, index=True)
    description: Optional[str] = SQLField(max_length=1000, default=None)
    status: TaskStatus = SQLField(default=TaskStatus.pending)
    priority: TaskPriority = SQLField(default=TaskPriority.medium)
    created_at: datetime = SQLField(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = SQLField(default=None)
    due_date: Optional[datetime] = SQLField(default=None)
    assigned_to: Optional[str] = SQLField(max_length=100, default=None)

# Pydantic models 
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    status: TaskStatus = Field(default=TaskStatus.pending, description="Task status")
    priority: TaskPriority = Field(default=TaskPriority.medium, description="Task priority")
    due_date: Optional[datetime] = Field(None, description="Task deadline")
    assigned_to: Optional[str] = Field(None, max_length=100, description="Assignee name")

    @validator('title')
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError('task title can not be empty')
        return v.strip()

    @validator('due_date')
    def validate_due_date(cls, v):
        if v and v <= datetime.utcnow():
            raise ValueError('Due date must be in the future')
        return v

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    status: Optional[TaskStatus] = Field(None, description="Task status")
    priority: Optional[TaskPriority] = Field(None, description="Task priority")
    due_date: Optional[datetime] = Field(None, description="Task deadline")
    assigned_to: Optional[str] = Field(None, max_length=100, description="Assignee name")

    @validator('title')
    def validate_title(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError('task title can not be empty')
            return v.strip()
        return v

    @validator('due_date')
    def validate_due_date(cls, v):
        if v and v <= datetime.utcnow():
            raise ValueError('Due date must be in the future')
        return v

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: Optional[datetime]
    due_date: Optional[datetime]
    assigned_to: Optional[str]

    class Config:
        from_attributes = True

