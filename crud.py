from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select
from models import Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority

def create_task(session: Session, task: TaskCreate) -> Task:
    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        assigned_to=task.assigned_to
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def get_task(session: Session, task_id: int) -> Optional[Task]:
    statement = select(Task).where(Task.id == task_id)
    return session.exec(statement).first()

def get_tasks(
    session: Session, 
    skip: int = 0, 
    limit: int = 100,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None
) -> List[Task]:
    statement = select(Task)
    
    if status:
        statement = statement.where(Task.status == status)
    if priority:
        statement = statement.where(Task.priority == priority)
    
    statement = statement.offset(skip).limit(limit)
    return session.exec(statement).all()

def get_tasks_by_status(session: Session, status: TaskStatus, skip: int = 0, limit: int = 100) -> List[Task]:
    statement = select(Task).where(Task.status == status).offset(skip).limit(limit)
    return session.exec(statement).all()

def get_tasks_by_priority(session: Session, priority: TaskPriority, skip: int = 0, limit: int = 100) -> List[Task]:
    statement = select(Task).where(Task.priority == priority).offset(skip).limit(limit)
    return session.exec(statement).all()

def update_task(session: Session, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
    db_task = get_task(session, task_id)
    if not db_task:
        return None
    
    update_data = task_update.dict(exclude_unset=True)
    
    update_data["updated_at"] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def delete_task(session: Session, task_id: int) -> bool:
    db_task = get_task(session, task_id)
    if not db_task:
        return False
    
    session.delete(db_task)
    session.commit()
    return True

def get_task_count(session: Session) -> int:
    statement = select(Task)
    return len(session.exec(statement).all()) 