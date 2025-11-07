"""
Service layer for task-related business logic.
"""
from typing import List, Optional

from backend.task.dto import TaskCreate, TaskDTO, TaskUpdate
from backend.task.exceptions import TaskAccessForbidden, TaskNotFound
from backend.task.models.task import TaskModel, TaskStatus
from backend.task.dependencies.repository import ITaskRepository


class TaskService:
    """
    Service for handling all task-related business logic.

    This service encapsulates the core application logic for managing tasks,
    including creation, retrieval, updates, and deletion. It is responsible
    for enforcing business rules, such as ownership, before delegating
    data persistence operations to the repository layer.

    Args:
        repo (ITaskRepository): The task repository dependency.
    """
    def __init__(self, repo: ITaskRepository):
        self.repo = repo

    @staticmethod
    def _to_dto(task_model: TaskModel) -> TaskDTO:
        """
        Converts a TaskModel SQLAlchemy instance to a TaskDTO.

        Args:
            task_model (TaskModel): The SQLAlchemy ORM model instance.

        Returns:
            TaskDTO: The corresponding Pydantic DTO.
        """
        return TaskDTO.model_validate(task_model)

    async def _get_and_verify_ownership(self, task_id: int, user_id: int) -> TaskModel:
        """
        A private helper to retrieve a task and verify user ownership.

        This is the central method for ensuring a user can only interact with
        their own tasks. It raises exceptions if the task is not found or if
        the user is not the owner.

        Args:
            task_id (int): The ID of the task to retrieve.
            user_id (int): The ID of the user requesting access.

        Returns:
            TaskModel: The validated task's SQLAlchemy model instance.

        Raises:
            TaskNotFound: If the task with the given ID does not exist.
            TaskAccessForbidden: If the user is not the owner of the task.
        """
        task = await self.repo.get_by_id(task_id)  # This will raise TaskNotFound if it fails
        if task.owner_id != user_id:
            raise TaskAccessForbidden
        return task

    async def get_tasks_for_user(
        self, user_id: int, status: Optional[TaskStatus] = None
    ) -> List[TaskDTO]:
        """
        Retrieves all tasks for a specific user.
        """
        tasks = await self.repo.get_all_for_user(user_id, status)
        return [self._to_dto(task) for task in tasks]

    async def get_task_by_id_for_user(self, task_id: int, user_id: int) -> TaskDTO:
        """
        Retrieves a single task for a user after verifying ownership.

        Args:
            task_id (int): The ID of the task to retrieve.
            user_id (int): The ID of the user requesting the task.

        Returns:
            TaskDTO: The DTO of the requested task.
        """
        task = await self._get_and_verify_ownership(task_id, user_id)
        return self._to_dto(task)

    async def create_task_for_user(
        self, task_create: TaskCreate, user_id: int
    ) -> TaskDTO:
        """
        Creates a new task owned by the specified user.
        """
        task = await self.repo.create(task_create, user_id)
        return self._to_dto(task)

    async def update_task(
        self, task_id: int, task_update: TaskUpdate, user_id: int
    ) -> TaskDTO:
        """
        Updates a task after verifying ownership.
        """
        await self._get_and_verify_ownership(task_id, user_id)
        updated_task = await self.repo.update(task_id, task_update)
        return self._to_dto(updated_task)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        """
        Deletes a task after verifying ownership.
        """
        await self._get_and_verify_ownership(task_id, user_id)
        await self.repo.delete(task_id)