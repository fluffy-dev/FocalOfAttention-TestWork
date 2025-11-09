"""
Service layer for task-related business logic.
"""
from typing import List, Optional

from backend.task.dto import TaskCreate, TaskDTO, TaskUpdate
from backend.task.exceptions import TaskAccessForbidden, TaskNotFound
from backend.task.models.task import TaskModel, TaskStatus
from backend.task.dependencies.repository import ITaskRepository
from task.entity import TaskEntity


class TaskService:
    """Service for handling all task-related business logic.

    This service encapsulates the core application logic for managing tasks,
    including creation, retrieval, updates, and deletion. It is responsible
    for enforcing business rules, such as ownership, before delegating
    data persistence operations to the repository layer.

    Attributes:
        repo (ITaskRepository): An instance of a task repository that conforms
            to the ITaskRepository interface, used for data access.
    """
    def __init__(self, repo: ITaskRepository):
        """Initializes the TaskService.

        Args:
            repo (ITaskRepository): The task repository dependency used for
                all data access operations.
        """
        self.repo = repo

    async def _get_and_verify(self, task_id: int, user_id: int) -> Optional[TaskDTO]:
        """Retrieves a task and verifies user ownership.

        This private helper method serves as a central point for access control.
        It fetches a task by its ID and then checks if the `owner_id` of the
        task matches the provided `user_id`. This ensures that users can only
        operate on their own tasks.

        Args:
            task_id (int): The ID of the task to retrieve.
            user_id (int): The ID of the user requesting access.

        Returns:
            TaskDTO: The data transfer object of the task if the user is
                verified as the owner. The type hint is Optional[TaskDTO] for
                flexibility, though the current implementation does not return
                None.

        Raises:
            TaskNotFound: If the task with the given ID does not exist
                (raised from the repository).
            TaskAccessForbidden: If the `user_id` does not match the task's
                `owner_id`.
        """
        task = await self.repo.get_by_id(task_id)

        if task.owner_id != user_id:
            raise TaskAccessForbidden

        return task

    async def get_tasks_for_user(
        self, user_id: int, status: Optional[TaskStatus] = None
    ) -> List[TaskDTO]:
        """Retrieves all tasks for a specific user, with optional filtering.

        Fetches a list of tasks associated with the given user ID. The list
        can be filtered to include only tasks of a specific status.

        Args:
            user_id (int): The ID of the user whose tasks to retrieve.
            status (Optional[TaskStatus]): If provided, filters tasks to only
                include those matching this status.

        Returns:
            List[TaskDTO]: A list of task data transfer objects belonging to
                the user.
        """
        return await self.repo.get_all_for_user(user_id, status)

    async def get_task_by_id_for_user(self, task_id: int, user_id: int) -> TaskDTO:
        """Retrieves a single task for a user after verifying ownership.

        This method ensures that the user requesting the task is its legitimate
        owner before returning it.

        Args:
            task_id (int): The ID of the task to retrieve.
            user_id (int): The ID of the user requesting the task.

        Returns:
            TaskDTO: The data transfer object of the requested task.

        Raises:
            TaskNotFound: If the task does not exist.
            TaskAccessForbidden: If the user is not the task's owner.
        """

        return await self._get_and_verify(task_id, user_id)

    async def create_task_for_user(
        self, dto: TaskCreate, user_id: int
    ) -> TaskDTO:
        """Creates a new task owned by the specified user.

        Takes task creation data, combines it with the owner's user ID to form
        a task entity, and passes it to the repository for creation.

        Args:
            dto (TaskCreate): A data transfer object containing the title and
                description for the new task.
            user_id (int): The ID of the user who will own the new task.

        Returns:
            TaskDTO: The data transfer object of the newly created task,
                including its generated ID.
        """
        entity = TaskEntity(
            owner_id=user_id,
            title=dto.title,
            description=dto.description,
        )
        return await self.repo.create(entity)

    async def update_task(
        self, task_id: int, task_update: TaskUpdate, user_id: int
    ) -> TaskDTO:
        """Updates a task after verifying ownership.

        This method first ensures the user owns the task and then delegates
        the update operation to the repository.

        Args:
            task_id (int): The ID of the task to update.
            task_update (TaskUpdate): A data transfer object with the fields
                to be updated.
            user_id (int): The ID of the user requesting the update.

        Returns:
            TaskDTO: The data transfer object of the updated task.

        Raises:
            TaskNotFound: If the task to update is not found.
            TaskAccessForbidden: If the user is not the task's owner.
        """
        await self._get_and_verify(task_id, user_id)
        return await self.repo.update(task_id, task_update)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        """Deletes a task after verifying ownership.

        This method confirms the user is the owner before instructing the
        repository to delete the task.

        Args:
            task_id (int): The ID of the task to delete.
            user_id (int): The ID of the user requesting the deletion.

        Raises:
            TaskNotFound: If the task to delete is not found.
            TaskAccessForbidden: If the user is not the task's owner.
        """
        await self._get_and_verify(task_id, user_id)
        await self.repo.delete(task_id)