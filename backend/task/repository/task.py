"""
Repository for task data access.
"""
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config.database import ISession
from backend.task.dto import TaskCreate, TaskUpdate
from backend.task.exceptions import TaskNotFound
from backend.task.models.task import TaskModel, TaskStatus


class TaskRepository:
    """
    Repository for task data access, operating with SQLAlchemy models.

    Args:
        session (ISession): The database session dependency.
    """
    def __init__(self, session: ISession):
        self.session: AsyncSession = session

    async def create(self, task_create: TaskCreate, owner_id: int) -> TaskModel:
        """
        Creates a new task record in the database.

        Args:
            task_create (TaskCreate): DTO with the data for the new task.
            owner_id (int): The ID of the user who owns the task.

        Returns:
            TaskModel: The newly created SQLAlchemy task model instance.
        """
        instance = TaskModel(**task_create.model_dump(), owner_id=owner_id)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get_by_id(self, task_id: int) -> TaskModel:
        """
        Retrieves a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve.

        Returns:
            TaskModel: The SQLAlchemy model instance for the task.

        Raises:
            TaskNotFound: If no task with the specified ID is found.
        """
        instance = await self.session.get(TaskModel, task_id)
        if instance is None:
            raise TaskNotFound
        return instance

    async def get_all_for_user(
        self, owner_id: int, status: Optional[TaskStatus] = None
    ) -> List[TaskModel]:
        """
        Retrieves all tasks for a specific user, with optional status filtering.

        Args:
            owner_id (int): The ID of the user whose tasks to retrieve.
            status (Optional[TaskStatus]): If provided, filters tasks by this status.

        Returns:
            List[TaskModel]: A list of task model instances.
        """
        stmt = select(TaskModel).where(TaskModel.owner_id == owner_id)
        if status:
            stmt = stmt.where(TaskModel.status == status)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, task_id: int, task_update: TaskUpdate) -> TaskModel:
        """
        Updates an existing task with new data.

        Args:
            task_id (int): The ID of the task to update.
            task_update (TaskUpdate): A DTO containing the fields to update.

        Returns:
            TaskModel: The updated SQLAlchemy task model instance.
        """
        task = await self.get_by_id(task_id)
        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete(self, task_id: int) -> None:
        """
        Deletes a task from the database.

        Args:
            task_id (int): The ID of the task to delete.
        """
        task = await self.get_by_id(task_id)
        await self.session.delete(task)
        await self.session.commit()
