from datetime import date, datetime
from .models import TaskStatus

def calculate_priority_score(days_open: int, revenue_potential: float, status: TaskStatus) -> float:
    """
    Calculate priority score based on the formula:
    priorityScore = daysOpen * 0.5 + revenuePotential * 0.3 + (status == "open" ? 50 : 0)
    """
    base_score = days_open * 0.5 + revenue_potential * 0.3
    status_bonus = 50 if status == TaskStatus.OPEN else 0
    return base_score + status_bonus

def calculate_days_open(created_date: datetime) -> int:
    """Calculate days since task was created"""
    if not created_date:
        return 0
    # Convert datetime to date for calculation
    created_date_only = created_date.date() if isinstance(created_date, datetime) else created_date
    return (date.today() - created_date_only).days 