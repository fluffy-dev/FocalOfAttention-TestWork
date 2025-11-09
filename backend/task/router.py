"""
Defines the RESTful API endpoints for task management.
"""
from typing import List, Optional
from fastapi import APIRouter, status, Depends, HTTPException

from backend.security.dependencies import ICurrentUser
from backend.task.dependencies.service import ITaskService
from backend.task.dto import TaskCreate, TaskDTO, TaskUpdate
from backend.task.models.task import TaskStatus
from backend.task.exceptions import TaskNotFound, TaskAccessForbidden

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/",
    response_model=TaskDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task"
)
async def create_task(
    task_data: TaskCreate,
    current_user: ICurrentUser,
    service: ITaskService,
):
    """
    Creates a new task for the currently authenticated user.

    The task is created with a 'pending' status by default and is
    explicitly owned by the user making the request.
    """
    return await service.create_task_for_user(task_data, current_user.id)


@router.get(
    "/",
    response_model=List[TaskDTO],
    summary="Get all tasks for the current user"
)
async def get_tasks(
    current_user: ICurrentUser,
    service: ITaskService,
    status: Optional[TaskStatus] = None,
):
    """
    Retrieves all tasks owned by the authenticated user.

    An optional `status` query parameter can be provided to filter the
    tasks by their current status (e.g., /tasks?status=pending).
    """
    return await service.get_tasks_for_user(current_user.id, status)


@router.get(
    "/{task_id}",
    response_model=TaskDTO,
    summary="Get a specific task by ID"
)
async def get_task_by_id(
    task_id: int,
    current_user: ICurrentUser,
    service: ITaskService,
):
    """
    Retrieves a single task by its ID.

    This endpoint will return a 404 Not Found if the task does not exist,
    or a 403 Forbidden if the task is not owned by the current user.
    """
    try:
        return await service.get_task_by_id_for_user(task_id, current_user.id)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found."
        )
    except TaskAccessForbidden:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task."
        )


@router.put(
    "/{task_id}",
    response_model=TaskDTO,
    summary="Update a task"
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: ICurrentUser,
    service: ITaskService,
):
    """
    Updates a task's title, description, or status.

    Only the owner of the task can perform this action. Trying to update
    another user's task will result in a 403 Forbidden error.
    """
    try:
        return await service.update_task(task_id, task_data, current_user.id)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found."
        )
    except TaskAccessForbidden:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task."
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task"
)
async def delete_task(
    task_id: int,
    current_user: ICurrentUser,
    service: ITaskService,
):
    """
    Deletes a task by its ID.

    Only the owner of the task can perform this action. This endpoint
    will return a 204 No Content on successful deletion.
    """
    try:
        await service.delete_task(task_id, current_user.id)
        return None
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found."
        )
    except TaskAccessForbidden:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task."
        )
