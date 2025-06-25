from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from .database import engine, get_db
from .models import Base, Task, TaskStatus
from .utils import calculate_priority_score, calculate_days_open

load_dotenv()

def create_db_and_tables():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    create_db_and_tables()
    yield
    # On shutdown
    print("Application shutting down.")

app = FastAPI(
    title="Sales Task Tracker API", 
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001,https://sales-tracker-frontend-k4us.onrender.com").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
from pydantic import BaseModel, ConfigDict
from datetime import date, datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    revenue_potential: float = 0.0
    contact_person: Optional[str] = None
    account: Optional[str] = None
    next_steps: Optional[str] = None
    due_date: Optional[date] = None
    status: TaskStatus = TaskStatus.OPEN

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    revenue_potential: Optional[float] = None
    contact_person: Optional[str] = None
    account: Optional[str] = None
    next_steps: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[TaskStatus] = None

class TaskResponse(TaskBase):
    id: int
    days_open: int
    priority_score: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

@app.get("/")
def read_root():
    return {"message": "Sales Task Tracker API"}

@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(
    status: Optional[TaskStatus] = None,
    account: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all tasks with optional filtering"""
    query = db.query(Task)
    
    if status:
        query = query.filter(Task.status == status)
    if account:
        query = query.filter(Task.account == account)
    
    tasks = query.order_by(Task.priority_score.desc()).all()
    
    # Update priority scores for all tasks
    for task in tasks:
        task.days_open = calculate_days_open(task.created_at)
        task.priority_score = calculate_priority_score(
            task.days_open, task.revenue_potential, task.status
        )
    
    db.commit()
    return tasks

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    print("Received task data:", task)
    """Create a new task"""
    task_data = task.model_dump()
    db_task = Task(**task_data)
    db_task.days_open = 0
    db_task.priority_score = calculate_priority_score(
        db_task.days_open, db_task.revenue_potential, db_task.status
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task by ID"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update priority score
    task.days_open = calculate_days_open(task.created_at)
    task.priority_score = calculate_priority_score(
        task.days_open, task.revenue_potential, task.status
    )
    db.commit()
    
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """Update a task"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    # Recalculate priority score
    db_task.days_open = calculate_days_open(db_task.created_at)
    db_task.priority_score = calculate_priority_score(
        db_task.days_open, db_task.revenue_potential, db_task.status
    )
    
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 