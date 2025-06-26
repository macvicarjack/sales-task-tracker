from sqlalchemy import Column, Integer, String, Float, Date, Enum, DateTime
from sqlalchemy.sql import func
from .database import Base
import enum

class TaskStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in-progress"
    CLOSED = "closed"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    revenue_potential = Column(Float, default=0.0)
    days_open = Column(Integer, default=0)
    priority_score = Column(Float, default=0.0)
    contact_person = Column(String)
    account = Column(String)
    next_steps = Column(String)
    due_date = Column(Date)
    status = Column(Enum(TaskStatus), default=TaskStatus.OPEN)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now()) 