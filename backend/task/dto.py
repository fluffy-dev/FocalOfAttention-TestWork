"""
Defines Data Transfer Objects (DTOs) for the Task module.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from backend.task.enums import TaskStatus


class TaskCreate(BaseModel):
    """
    DTO for creating a new task.
    """
    title: str = Field(..., min_length=1, max_length=255, description="The title of the task.")
    description: Optional[str] = Field(None, description="The optional description of the task.")


class TaskUpdate(BaseModel):
    """
    DTO for updating an existing task. All fields are optional.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskDTO(BaseModel):
    """
    DTO for representing a task in API responses.
    """
    id: int
    title: str = Field(..., min_length=1, max_length=255, description="The title of the task.")
    description: Optional[str] = Field(None, description="The optional description of the task.")
    status: TaskStatus
    owner_id: int

    class Config:
        """Pydantic configuration to allow ORM model mapping."""
        from_attributes = True
