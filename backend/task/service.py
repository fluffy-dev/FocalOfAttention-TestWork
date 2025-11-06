"""
Service layer for task-related business logic.
"""
from typing import List, Optional

from backend.task.dto import TaskCreate, TaskDTO, TaskUpdate
from backend.task.exceptions import TaskAccessForbidden
from backend.task.models.task import TaskModel, TaskStatus
from backend.task.dependencies.repository import ITaskRepository


class TaskService:
    """
    Service for handling task-related business logic.

    Args:
        repo (ITaskRepository): The task repository dependency.
    """
    def __init__(self, repo: ITaskRepository):
        self.repo = repo

    @staticmethod
    def _to_dto(task_model: TaskModel) -> TaskDTO:
        """Converts a TaskModel to a TaskDTO."""
        return TaskDTO.model_validate(task_model)

    async def get_tasks_for_user(
        self, user_id: int, status: Optional[TaskStatus] = None
    ) -> List[TaskDTO]:
        """
        Retrieves all tasks for a specific user.

        Args:
            user_id (int): The ID of the user.
            status (Optional[TaskStatus]): Optional status to filter tasks by.

        Returns:
            List[TaskDTO]: A list of task DTOs.
        """
        tasks = await self.repo.get_all_for_user(user_id, status)
        return [self._to_dto(task) for task in tasks]

    async def create_task_for_user(
        self, task_create: TaskCreate, user_id: int
    ) -> TaskDTO:
        """
        Creates a new task owned by the specified user.

        Args:
            task_create (TaskCreate): The data for the new task.
            user_id (int): The ID of the owning user.

        Returns:
            TaskDTO: The DTO of the newly created task.
        """
        task = await self.repo.create(task_create, user_id)
        return self._to_dto(task)

    async def update_task(
        self, task_id: int, task_update: TaskUpdate, user_id: int
    ) -> TaskDTO:
        """
        Updates a task after verifying ownership.

        Args:
            task_id (int): The ID of the task to update.
            task_update (TaskUpdate): The data to update.
            user_id (int): The ID of the user attempting the update.

        Returns:
            TaskDTO: The DTO of the updated task.

        Raises:
            TaskAccessForbidden: If the user does not own the task.
        """
        task = await self.repo.get_by_id(task_id)
        if task.owner_id != user_id:
            raise TaskAccessForbidden("User does not have permission to update this task.")
        updated_task = await self.repo.update(task_id, task_update)
        return self._to_dto(updated_task)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        """
        Deletes a task after verifying ownership.

        Args:
            task_id (int): The ID of the task to delete.
            user_id (int): The ID of the user attempting the deletion.

        Raises:
            TaskAccessForbidden: If the user does not own the task.
        """
        task = await self.repo.get_by_id(task_id)
        if task.owner_id != user_id:
            raise TaskAccessForbidden("User does not have permission to delete this task.")
        await self.repo.delete(task_id)