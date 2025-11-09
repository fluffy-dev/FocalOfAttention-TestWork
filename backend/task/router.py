"""Defines the RESTful API endpoints for task management.

This module sets up a FastAPI APIRouter to handle all task-related
HTTP requests. It defines endpoints for creating, retrieving, updating, and
deleting tasks (CRUD operations). All endpoints are protected and require an
authenticated user, whose identity is injected via the `ICurrentUser`
dependency. The business logic is delegated to the `ITaskService` dependency,
keeping the routing layer clean and focused on API contract definition.
"""
from typing import List, Optional
from fastapi import APIRouter, status

from backend.security.dependencies import ICurrentUser
from backend.task.dependencies.service import ITaskService
from backend.task.dto import TaskCreate, TaskDTO, TaskUpdate
from backend.task.models.task import TaskStatus

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
    """Creates a new task for the currently authenticated user.

    The task is created with a 'pending' status by default and is
    explicitly owned by the user making the request. The request body
    should contain the title and description of the task.

    Args:
        task_data (TaskCreate): A Pydantic model containing the data for the
            new task (title, description).
        current_user (ICurrentUser): The dependency that provides the currently
            authenticated user's data.
        service (ITaskService): The dependency that provides the task business
            logic service.

    Returns:
        TaskDTO: A Pydantic model representing the newly created task,
            including its system-generated ID and default status.
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
    task_status: Optional[TaskStatus] = None,
):
    """Retrieves all tasks owned by the authenticated user.

    An optional `status` query parameter can be provided to filter the
    tasks by their current status (e.g., /tasks?status=pending). If no
    status is provided, all tasks for the user are returned.

    Args:
        current_user (ICurrentUser): The dependency providing the authenticated
            user's data.
        service (ITaskService): The dependency for the task business logic.
        task_status (Optional[TaskStatus]): An optional query parameter to
            filter tasks by their status (e.g., 'pending', 'in_progress').

    Returns:
        List[TaskDTO]: A list of tasks belonging to the user that match the
            filter criteria.
    """
    return await service.get_tasks_for_user(current_user.id, task_status)


@router.get(
    "/{task_id}",
    response_model=TaskDTO,
    status_code=status.HTTP_200_OK,
    summary="Get a specific task by ID"
)
async def get_task_by_id(
    task_id: int,
    current_user: ICurrentUser,
    service: ITaskService,
):
    """Retrieves a single task by its ID.

    This endpoint will return a 404 Not Found if the task does not exist,
    or a 403 Forbidden if the task is not owned by the current user.

    Args:
        task_id (int): The unique identifier of the task to retrieve,
            passed as a path parameter.
        current_user (ICurrentUser): The dependency providing the authenticated
            user's data.
        service (ITaskService): The dependency for the task business logic.

    Returns:
        TaskDTO: The data transfer object for the requested task.
    """
    return await service.get_task_by_id_for_user(task_id, current_user.id)


@router.put(
    "/{task_id}",
    response_model=TaskDTO,
    status_code=status.HTTP_200_OK,
    summary="Update a task"
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: ICurrentUser,
    service: ITaskService,
):
    """Updates a task's title, description, or status.

    Only the owner of the task can perform this action. The request body can
    contain any combination of the updatable fields. Trying to update
    another user's task will result in a 403 Forbidden error.

    Args:
        task_id (int): The unique identifier of the task to update.
        task_data (TaskUpdate): A Pydantic model containing the fields to
            be updated.
        current_user (ICurrentUser): The dependency providing the authenticated
            user's data.
        service (ITaskService): The dependency for the task business logic.

    Returns:
        TaskDTO: The data transfer object representing the updated state of the
            task.
    """
    return await service.update_task(task_id, task_data, current_user.id)


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
    """Deletes a task by its ID.

    Only the owner of the task can perform this action. This endpoint
    will return a 204 No Content on successful deletion, with an empty
    response body.

    Args:
        task_id (int): The unique identifier of the task to be deleted.
        current_user (ICurrentUser): The dependency providing the authenticated
            user's data.
        service (ITaskService): The dependency for the task business logic.
    """
    await service.delete_task(task_id, current_user.id)